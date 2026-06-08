import time
import psutil
import GPUtil
import os
from collections import defaultdict
from models.models import *
import win32process
import win32gui
import win32con

SYSTEM_PROCESS_NAMES = {
    "ms", "Microsoft", "System", "Idle", "Registry", "smss.exe", "csrss.exe", "wininit.exe", "services.exe", "lsass.exe", "svchost.exe",
    "fontdrvhost.exe", "winlogon.exe", "dwm.exe", "sihost.exe", "RuntimeBroker.exe", "taskhostw.exe", "explorer.exe",
    "SearchHost.exe", "StartMenuExperienceHost.exe", "ShellExperienceHost.exe", "TextInputHost.exe", "SecurityHealthSystray.exe", "ctfmon.exe"
}

WINDOWS_DIRS = [os.environ.get('SystemRoot', r'C:\Windows').lower(),
                os.path.join(os.environ.get('SystemRoot', r'C:\Windows'), 'System32').lower()]

def is_system_process(proc):
    try:
        name = proc.info.get("name", "")
        exe = proc.info.get("exe", "") or ""
        if name in SYSTEM_PROCESS_NAMES:
            return True
        exe_lower = exe.lower()
        for win_dir in WINDOWS_DIRS:
            if exe_lower.startswith(win_dir):
                return True
        return False
    except Exception:
        return True  # If we can't access info, treat as system

def get_visible_pids():
    visible_pids = set()
    def enum_handler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                visible_pids.add(pid)
            except Exception:
                pass
    win32gui.EnumWindows(enum_handler, None)
    return visible_pids


class ProcessManager:
    def __init__(self):
        self.processes : list[ProcInfo] = [] 
        self.sys_info = None
        # Initialize CPU percent for all processes (non-blocking)
        for proc in psutil.process_iter(['pid']):
            try:
                proc.cpu_percent(interval=None)
            except Exception:
                pass

    def _get_process_info(self, proc, visible_pids):
        try:
            if is_system_process(proc):
                return None
            if proc.pid not in visible_pids:
                return None
            info = proc.as_dict(attrs=["pid", "name", "exe", "memory_full_info"])
            if info["memory_full_info"] is None or not info["exe"]:
                return None
            cpu = proc.cpu_percent(interval=0.0)  # Non-blocking
            return {
                "pid": info["pid"],
                "name": info["name"],
                "exe": info["exe"],
                "mem": info["memory_full_info"].private / (1024**2),
                "cpu": cpu
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
            return None

    def update_processes(self):
        # Use a generator to avoid blocking the UI
        def iter_processes_chunked(attrs, chunk_size=10):
            chunk = []
            for proc in psutil.process_iter(attrs):
                chunk.append(proc)
                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []
            if chunk:
                yield chunk

        visible_pids = get_visible_pids()
        proc_infos = []
        # Process in small chunks to avoid blocking
        for chunk in iter_processes_chunked(["pid", "name", "exe", "memory_full_info"], chunk_size=5):
            for proc in chunk:
                info = self._get_process_info(proc, visible_pids)
                if info is not None:
                    proc_infos.append(info)
            # Yield to other threads/UI (very short sleep)
            time.sleep(0.001)
        # Group by exe path
        grouped = defaultdict(lambda: {"pids": [], "name": "", "exe": "", "mem": 0.0, "cpu": 0.0})
        for info in proc_infos:
            exe = info["exe"]
            grouped[exe]["pids"].append(info["pid"])
            grouped[exe]["name"] = info["name"]
            grouped[exe]["exe"] = exe
            grouped[exe]["mem"] += info["mem"]
            grouped[exe]["cpu"] += info["cpu"]
        self.processes.clear()
        for exe, data in grouped.items():
            self.processes.append(ProcInfo(
                pids=data["pids"],
                name=data["name"],
                exe=data["exe"],
                mem_usage=data["mem"],
                cpu_usage=data["cpu"]
            ))
        self.processes.sort(key=lambda x: x.cpu_usage, reverse=True)


    def update_sys_info(self):
        """Update system information"""
        try:
            sys_info = SysInfo(
                psutil.cpu_percent(interval=None),
                psutil.virtual_memory().percent,
                self.get_gpu_usage()[0],
                psutil.disk_usage('/').percent,
            )

            self.sys_info = sys_info
            return sys_info
        except Exception as e:
            print(f"Error updating system info: {e}")
            return self.sys_info
    

    def get_gpu_usage(self):
        """Get GPU usage information"""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return round(gpus[0].load * 100, 1), gpus[0].name
        except Exception:
            pass
        return 0, ""

    def __del__(self):
        """Clean up thread pool on deletion"""
        pass  # No executor to shutdown, handled in method


# pm = ProcessManager()
# pm.update_processes()
# pm.update_processes()
# for proc in pm.processes:
#     if proc.cpu_usage > 0:
#         print(proc)


import customtkinter as ctk
import psutil

from models.models import ProcInfo
from ui.buttons.buttons import *

class ProcessFrame(ctk.CTkFrame):
    def __init__(self, parent, proc_info: ProcInfo, **kwargs):
        super().__init__(master=parent, **kwargs)
        self.proc_info = proc_info

        # Configure grid columns
        self.grid_columnconfigure(0, weight=1)  # Info label column expands
        self.grid_columnconfigure(1, weight=0)  # Buttons don't expand
        self.grid_columnconfigure(2, weight=0)

        # Configure frame to fill horizontally
        self.grid(sticky="ew", pady=5, padx=5)

        # Process info label with instance count
        instance_count = len(proc_info.pids)
        instances_text = f" ({instance_count} instances)" if instance_count > 1 else ""
        info_text = f"{proc_info.name}{instances_text}\nCPU: {proc_info.cpu_usage:.1f}% | RAM: {proc_info.mem_usage:.1f} MB\n"
        label = ctk.CTkLabel(self, text=info_text, anchor="w", justify="left")
        label.grid(row=0, column=0, padx=10, sticky="w")

        # Maximize button
        btn_focus = GrayButton(self, text="Maximize", width=80, command=self.focus_window_placeholder)
        btn_focus.grid(row=0, column=1, padx=5)

        # Kill button
        btn_kill = RedButton(self, text="Kill", width=60, command=self.terminate_all)
        btn_kill.grid(row=0, column=2, padx=5)

    def terminate_all(self):
        """Terminate all instances of the process"""
        for pid in self.proc_info.pids:
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                self.destroy()
            except psutil.NoSuchProcess:
                # Process might have already terminated
                continue
            except psutil.AccessDenied:
                # Try to kill if terminate doesn't work
                try:
                    proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

    def focus_window_placeholder(self):
        print("Window focus not implemented yet")

    def update_from_proc(self, proc):
        """Update the displayed info with new proc data."""
        self.proc = proc
        # Update any labels or widgets here. Adjust attribute names as needed:
        if hasattr(self, 'name_label'):
            self.name_label.configure(text=proc.name)
        if hasattr(self, 'cpu_label'):
            self.cpu_label.configure(text=f"{getattr(proc, 'cpu_usage', 0):.1f}%")
        if hasattr(self, 'mem_label'):
            self.mem_label.configure(text=f"{getattr(proc, 'mem_usage', 0):.1f} MB")
        # ...update other widgets as needed...
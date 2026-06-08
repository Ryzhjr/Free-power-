from dataclasses import dataclass

@dataclass
class ProcInfo:
    pids: list[int]  # List of process IDs for all instances
    name: str        # Process name
    exe: str         # Executable path
    mem_usage: float # Combined memory usage
    cpu_usage: float # Combined CPU usage


@dataclass
class SysInfo:
    cpu_usage: float
    mem_usage: float
    gpu_usage: float
    disk_usage: float
import customtkinter as ctk
import threading
import time
import os
import json
from winotify import Notification, audio

from process_manager import ProcessManager
from ui.buttons.buttons import *
from utils.constants import UTILS, COLOR, FONT
from ui.windows.settings_window import SettingsWindow
from ui.windows.help_window import HelpWindow


class GlobalInfoFrame(ctk.CTkFrame):
    def __init__(self, parent, proc_manager: "ProcessManager", **kwargs):
        super().__init__(master=parent, width=250, **kwargs)
        self.proc_manager = proc_manager
        self.running = True
        
        # Create notification cooldown tracker
        self.last_notifications = {
            'cpu': 0,
            'ram': 0,
            'gpu': 0,
            'disk': 0
        }
        
        # Create update thread
        self.update_thread = threading.Thread(target=self.update_thread_func, daemon=True)

        # Configure grid columns and rows to expand properly
        self.grid_columnconfigure(1, weight=1)  # Column for progress bars
        self.grid_rowconfigure(8, weight=1) 
        self.grid_propagate(False)

        # CPU
        self.label_cpu = ctk.CTkLabel(self, text="CPU", font=FONT.DEFAULT)
        self.label_cpu.grid(row=0, column=0, sticky="w", padx=5, pady=(40, 10))
        self.cpu_percent = ctk.CTkLabel(self, text="0%", font=FONT.DEFAULT)
        self.cpu_percent.grid(row=0, column=2, sticky="e", padx=5, pady=(40, 10))
        self.cpu_bar = ctk.CTkProgressBar(self, width=180, height=15)
        self.cpu_bar.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 40))

        # RAM
        self.label_ram = ctk.CTkLabel(self, text="RAM", font=FONT.DEFAULT)
        self.label_ram.grid(row=2, column=0, sticky="w", padx=5, pady=(0, 10))
        self.ram_percent = ctk.CTkLabel(self, text="0%", font=FONT.DEFAULT)
        self.ram_percent.grid(row=2, column=2, sticky="e", padx=5, pady=(0, 10))
        self.ram_bar = ctk.CTkProgressBar(self, width=180, height=15)
        self.ram_bar.grid(row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 40))

        # GPU
        self.label_gpu = ctk.CTkLabel(self, text=f"GPU", font=FONT.DEFAULT)
        self.label_gpu.grid(row=4, column=0, sticky="w", padx=5, pady=(0, 10))
        self.gpu_percent = ctk.CTkLabel(self, text="0%", font=FONT.DEFAULT)
        self.gpu_percent.grid(row=4, column=2, sticky="e", padx=5, pady=(0, 10))
        self.gpu_bar = ctk.CTkProgressBar(self, width=180, height=15)
        self.gpu_bar.grid(row=5, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 40))

        # Disk
        self.label_disk = ctk.CTkLabel(self, text="Disk Space", font=FONT.DEFAULT)
        self.label_disk.grid(row=6, column=0, sticky="w", padx=5, pady=(0, 10))
        self.disk_percent = ctk.CTkLabel(self, text="0%", font=FONT.DEFAULT)
        self.disk_percent.grid(row=6, column=2, sticky="e", padx=5, pady=(0, 10))
        self.disk_bar = ctk.CTkProgressBar(self, width=180, height=15)
        self.disk_bar.grid(row=7, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 40))

        # Frame for buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=9, column=0, columnspan=2, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0,1), weight=1)

        # Settings button
        self.settings_button = GrayButton(self.button_frame, text="⚙ Settings", command=self.open_settings)
        self.settings_button.grid(row=0, column=0, padx=5, sticky="ew")

        # Help button
        self.help_button = GrayButton(self.button_frame, text="❔ Help", command=self.open_help)
        self.help_button.grid(row=0, column=1, padx=5, sticky="ew")

        # Position the frame itself
        self.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Start update thread
        self.update_thread.start()


    def open_settings(self):
        SettingsWindow(self)

    def open_help(self):
        HelpWindow(self)


    def update_thread_func(self):
        while self.running:
            # Get system information
            sys_info = self.proc_manager.update_sys_info()
            
            # Schedule UI updates in main thread
            self.after(0, lambda: self.update_ui(sys_info))
            
            # Sleep for update interval
            time.sleep(UTILS.RELOAD_INTERVAL)
    

    def update_ui(self, sys_info):
        """Updates UI elements with new system information"""
        # Update CPU
        self.cpu_percent.configure(text=f"{sys_info.cpu_usage:.1f}%")
        self.cpu_bar.set(sys_info.cpu_usage / 100)
        self.cpu_bar.configure(progress_color=COLOR.BAR_OK if sys_info.cpu_usage < UTILS.WARNING_THRESHOLD else COLOR.BAR_WARNING)
        
        # Update RAM
        self.ram_percent.configure(text=f"{sys_info.mem_usage:.1f}%")
        self.ram_bar.set(sys_info.mem_usage / 100)
        self.ram_bar.configure(progress_color=COLOR.BAR_OK if sys_info.mem_usage < UTILS.WARNING_THRESHOLD else COLOR.BAR_WARNING)
        
        # Update GPU
        self.gpu_percent.configure(text=f"{sys_info.gpu_usage:.1f}%")
        self.gpu_bar.set(sys_info.gpu_usage / 100)
        self.gpu_bar.configure(progress_color=COLOR.BAR_OK if sys_info.gpu_usage < UTILS.WARNING_THRESHOLD else COLOR.BAR_WARNING)
        
        # Update Disk
        self.disk_percent.configure(text=f"{sys_info.disk_usage:.1f}%")
        self.disk_bar.set(sys_info.disk_usage / 100)
        self.disk_bar.configure(progress_color=COLOR.BAR_OK if sys_info.disk_usage < UTILS.WARNING_THRESHOLD else COLOR.BAR_WARNING)

        # Check for notifications
        self._check_notifications(sys_info)


    def _check_notifications(self, sys_info):
        """Shows notifications for high resource usage"""
        if not UTILS.NOTIFICATIONS_ENABLED:
            return

        current_time = time.time()
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "warning.ico")

        def show_notification(resource, title, message):
            if current_time - self.last_notifications[resource] >= UTILS.NOTIFICATION_COOLDOWN:
                toast = Notification(
                    app_id="FreePower Task Manager",
                    title=title,
                    msg=message,
                    icon=icon_path,  # Add icon if file exists
                    duration="short"
                )
                toast.set_audio(audio.Default, loop=False)
                toast.show()
                self.last_notifications[resource] = current_time

        if sys_info.cpu_usage >= UTILS.WARNING_THRESHOLD:
            show_notification('cpu', "High CPU Usage", f"CPU usage is at {sys_info.cpu_usage:.1f}%!")
        
        if sys_info.mem_usage >= UTILS.WARNING_THRESHOLD:
            show_notification('ram', "High RAM Usage", f"RAM usage is at {sys_info.mem_usage:.1f}%!")
        
        if sys_info.gpu_usage >= UTILS.WARNING_THRESHOLD:
            show_notification('gpu', "High GPU Usage", f"GPU usage is at {sys_info.gpu_usage:.1f}%!")
        
        if sys_info.disk_usage >= UTILS.WARNING_THRESHOLD:
            show_notification('disk', "High Disk Usage", f"Disk usage is at {sys_info.disk_usage:.1f}%!")


    def destroy(self):
        """Clean up when the frame is destroyed"""
        self.running = False
        if self.update_thread.is_alive():
            self.update_thread.join(timeout=1.0)
        super().destroy()
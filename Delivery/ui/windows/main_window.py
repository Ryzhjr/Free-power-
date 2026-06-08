import customtkinter as ctk

from process_manager import ProcessManager
from ui.frames.g_info_frame import GlobalInfoFrame
from ui.frames.processes_frame import ProcessesFrame
from ui.windows.settings_window import SettingsWindow
from utils.constants import UTILS

class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FreePower Task Manager")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.iconbitmap("assets/icon.ico")

        # Load saved settings
        SettingsWindow.load_settings()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create process manager first
        self.process_manager = ProcessManager()

        self.processes_frame = None
        self.g_info_frame = None

        # Update theme from settings
        ctk.set_appearance_mode(UTILS.THEME)


    def _apply_theme(self):
        """Apply the current theme"""
        ctk.set_appearance_mode(UTILS.THEME)
        self.update_idletasks()


    def refresh_theme(self):
        """Update the application's theme"""
        self._apply_theme()
        # Destroy and recreate frames to ensure they get the new theme
        if self.processes_frame:
            self.processes_frame.destroy()
        if self.g_info_frame:
            self.g_info_frame.destroy()
        
        # Recreate frames with process manager
        self.processes_frame = ProcessesFrame(self, self.process_manager)
        self.g_info_frame = GlobalInfoFrame(self, self.process_manager)
    
    def run(self):
        # Create frames with process manager
        self.processes_frame = ProcessesFrame(self, self.process_manager)
        self.g_info_frame = GlobalInfoFrame(self, self.process_manager)
        self.mainloop()
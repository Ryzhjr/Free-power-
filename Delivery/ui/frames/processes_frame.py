import customtkinter as ctk
import threading
import time
import psutil
from utils.constants import UTILS
from ui.frames.process_frame import ProcessFrame

class ProcessesFrame(ctk.CTkFrame):
    def __init__(self, parent, process_manager, **kwargs):
        super().__init__(master=parent, **kwargs)
        self.process_manager = process_manager
        self.running = True

        # Configure grid column to expand
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Search entry
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search")
        self.search_entry.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.filter_processes)

        # Scrollable frame for processes
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=560, height=400)
        self.scroll_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Position the frame itself
        self.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Initialize CPU monitoring
        psutil.cpu_percent(interval=None, percpu=True)
        time.sleep(0.1)  # Short sleep for initial CPU measurements

        # Start process update thread
        self.process_thread = threading.Thread(target=self.update_thread_func, daemon=True)
        self.process_thread.start()

    def filter_processes(self, event=None):
        """Filter processes based on search text"""
        print("Filter called") # Debug print
        self._update_display()

    def _update_display(self):
        """Update the display with current processes"""
        print("Updating display") # Debug print
        search_text = self.search_entry.get().lower()
        
        # Clear all current frames
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        # Display processes
        print(f"Process count: {len(self.process_manager.processes)}") # Debug print
        for proc in self.process_manager.processes:
            if not search_text or search_text in proc.name.lower():
                try:
                    ProcessFrame(self.scroll_frame, proc)
                except Exception as e:
                    print(f"Error creating process frame: {e}")


    def update_thread_func(self):
        while self.running:
            self.process_manager.update_processes()
            # Schedule UI update in main thread
            self.after(0, self._update_display)
            time.sleep(UTILS.RELOAD_INTERVAL)

    def destroy(self):
        """Clean up when the frame is destroyed"""
        self.running = False
        if self.process_thread.is_alive():
            self.process_thread.join(timeout=1.0)
        super().destroy()
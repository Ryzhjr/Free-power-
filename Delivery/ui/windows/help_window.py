import customtkinter as ctk
from utils.constants import HELP, FONT

class HelpWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure window
        self.title("Aide - FreePower Task Manager")
        self.geometry("600x600")
        self.resizable(False, False)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add text widget
        self.text = ctk.CTkTextbox(self.main_frame, width=580, height=380)
        self.text.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Insert help text
        self.text.insert("1.0", HELP.TEXT)
        self.text.configure(state="disabled")  # Make text read-only

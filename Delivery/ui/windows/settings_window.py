import customtkinter as ctk
from tkinter import messagebox
import json
import os

from ui.buttons.buttons import *
from utils.constants import UTILS, COLOR


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("400x400")  # Made taller for new setting
        self.parent = parent

        # Make window modal
        self.transient(parent)
        self.grab_set()

        # Store initial theme for cancellation
        self.initial_theme = UTILS.THEME
        
        # Refresh interval
        refresh_frame = ctk.CTkFrame(self)
        refresh_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(refresh_frame, text="Refresh interval (seconds):").pack(side="left", padx=10)
        self.refresh_entry = ctk.CTkEntry(refresh_frame, width=100)
        self.refresh_entry.pack(side="right", padx=10)
        self.refresh_entry.insert(0, str(UTILS.RELOAD_INTERVAL))

        # Warning threshold
        threshold_frame = ctk.CTkFrame(self)
        threshold_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(threshold_frame, text="Warning threshold (%):").pack(side="left", padx=10)
        self.threshold_entry = ctk.CTkEntry(threshold_frame, width=100)
        self.threshold_entry.pack(side="right", padx=10)
        self.threshold_entry.insert(0, str(UTILS.WARNING_THRESHOLD))

        # Notifications Frame
        notifications_frame = ctk.CTkFrame(self)
        notifications_frame.pack(fill="x", padx=20, pady=10)
        
        # Notifications checkbox
        self.notifications_var = ctk.BooleanVar(value=UTILS.NOTIFICATIONS_ENABLED)
        self.notifications_checkbox = ctk.CTkCheckBox(
            notifications_frame, 
            text="Enable notifications",
            variable=self.notifications_var
        )
        self.notifications_checkbox.pack(pady=5)

        # Notification cooldown
        cooldown_frame = ctk.CTkFrame(notifications_frame)
        cooldown_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(cooldown_frame, text="Notification cooldown (minutes):").pack(side="left", padx=10)
        self.cooldown_entry = ctk.CTkEntry(cooldown_frame, width=100)
        self.cooldown_entry.pack(side="right", padx=10)
        self.cooldown_entry.insert(0, str(UTILS.NOTIFICATION_COOLDOWN // 60))  # Convert seconds to minutes

        # Theme preference
        theme_frame = ctk.CTkFrame(self)
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(theme_frame, text="Theme:").pack(side="left", padx=10)
        self.theme_var = ctk.StringVar(value=UTILS.THEME)
        self.light_theme_rb = ctk.CTkRadioButton(
            theme_frame, 
            text="Light",
            variable=self.theme_var,
            value="light"
        )
        self.light_theme_rb.pack(side="left", padx=10)
        
        self.dark_theme_rb = ctk.CTkRadioButton(
            theme_frame, 
            text="Dark",
            variable=self.theme_var,
            value="dark"
        )
        self.dark_theme_rb.pack(side="left", padx=10)

        # Buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)

        # Save and Cancel buttons
        cancel_btn = GrayButton(button_frame, text="Cancel", command=self.cancel)
        cancel_btn.pack(side="left", padx=10)

        save_btn = GreenButton(button_frame, text="Save", command=self.save_settings)
        save_btn.pack(side="left", padx=10)


    def cancel(self):
        """Restore initial theme and close"""
        UTILS.THEME = self.initial_theme
        self.destroy()


    def save_settings(self):
        try:
            new_interval = float(self.refresh_entry.get())
            new_threshold = int(self.threshold_entry.get())
            new_cooldown = int(self.cooldown_entry.get()) * 60  # Convert minutes to seconds
            
            if new_interval <= 0 or new_threshold <= 0 or new_threshold > 100 or new_cooldown < 0:
                raise ValueError("Invalid values")
                
            UTILS.RELOAD_INTERVAL = new_interval
            UTILS.WARNING_THRESHOLD = new_threshold
            UTILS.NOTIFICATIONS_ENABLED = self.notifications_var.get()
            UTILS.NOTIFICATION_COOLDOWN = new_cooldown
            UTILS.THEME = self.theme_var.get()
            
            # Save to JSON file
            settings = {
                "reload_interval": new_interval,
                "warning_threshold": new_threshold,
                "notifications_enabled": UTILS.NOTIFICATIONS_ENABLED,
                "notification_cooldown": new_cooldown,
                "theme": UTILS.THEME
            }
            
            settings_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config")
            os.makedirs(settings_dir, exist_ok=True)
            settings_file = os.path.join(settings_dir, "settings.json")
            
            with open(settings_file, "w") as f:
                json.dump(settings, f, indent=4)

            # Destroy window first
            self.destroy()
            
            # Schedule theme refresh after window is destroyed
            self.parent.after(100, self._apply_theme_change)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid values:\n- Interval must be a positive number\n- Threshold must be between 1 and 100\n- Cooldown must be a positive number")


    def _apply_theme_change(self):
        """Apply theme change after window is destroyed"""
        # Set the theme
        ctk.set_appearance_mode(UTILS.THEME)
        # Tell main window to refresh
        if hasattr(self.parent, 'refresh_theme'):
            self.parent.refresh_theme()


    @staticmethod
    def load_settings():
        try:
            settings_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "settings.json")
            
            if os.path.exists(settings_file):
                with open(settings_file, "r") as f:
                    settings = json.load(f)
                    
                UTILS.RELOAD_INTERVAL = float(settings.get("reload_interval", UTILS.RELOAD_INTERVAL))
                UTILS.WARNING_THRESHOLD = int(settings.get("warning_threshold", UTILS.WARNING_THRESHOLD))
                UTILS.NOTIFICATIONS_ENABLED = bool(settings.get("notifications_enabled", UTILS.NOTIFICATIONS_ENABLED))
                UTILS.NOTIFICATION_COOLDOWN = int(settings.get("notification_cooldown", UTILS.NOTIFICATION_COOLDOWN))
                UTILS.THEME = settings.get("theme", UTILS.THEME)
                
                # Apply theme immediately after loading
                ctk.set_appearance_mode(UTILS.THEME)
                
        except Exception as e:
            print(f"Error loading settings: {e}")

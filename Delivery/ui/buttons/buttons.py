import customtkinter as ctk

from utils.constants import *


class GreenButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("fg_color", COLOR.PRIMARY_GREEN)
        kwargs.setdefault("hover_color", COLOR.HOVER_GREEN)
        # wargs.setdefault("text_color", "#E5E5E5")
        super().__init__(*args, **kwargs)


class RedButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("fg_color", COLOR.PRIMARY_RED)
        kwargs.setdefault("hover_color", COLOR.HOVER_RED)
        # wargs.setdefault("text_color", "#E5E5E5")
        super().__init__(*args, **kwargs)


class GrayButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("fg_color", COLOR.PRIMARY_GRAY)
        kwargs.setdefault("hover_color", COLOR.HOVER_GRAY)
        # wargs.setdefault("text_color", "#E5E5E5")
        super().__init__(*args, **kwargs)
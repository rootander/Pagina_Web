import tkinter as tk
from tkinter import messagebox, ttk
import os
import cv2
from PIL import Image, ImageTk
import face_recognition
import time
from datetime import datetime


class Config:
    PRIMARY_COLOR = "#6A5ACD"
    SECONDARY_COLOR = "#9370DB"
    ACCENT_COLOR = "#00CED1"
    BG_COLOR = "#F8F9FA"
    CARD_COLOR = "#FFFFFF"
    TEXT_COLOR = "#2D3748"
    SUCCESS_COLOR = "#48BB78"
    ERROR_COLOR = "#E53E3E"
    TITLE_FONT = ("Segoe UI", 24, "bold")
    SUBTITLE_FONT = ("Segoe UI", 16)
    BUTTON_FONT = ("Segoe UI", 12)
    LABEL_FONT = ("Segoe UI", 11)
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    FACE_MATCH_THRESHOLD = 0.6
    LOGIN_DURATION = 10
    FACE_TOLERANCE = 0.6


class Utilities:
    @staticmethod
    def center_window(window, width, height):
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    @staticmethod
    def usuario_jpg(nombre):
        return f"faces/{nombre}.jpg"
    
    @staticmethod
    def ensure_directories():
        os.makedirs("faces", exist_ok=True)
        os.makedirs("temp", exist_ok=True)
    
    @staticmethod
    def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)


class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, width=200, height=40, bg=Config.PRIMARY_COLOR, fg="white", font=Config.BUTTON_FONT, hover_bg=Config.SECONDARY_COLOR, *args, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, *args, **kwargs)
        self.command = command
        self.bg = bg
        self.hover_bg = hover_bg
        self.fg = fg
        self.font = font
        self.text = text
        self.width = width
        self.height = height
        
        self.rect_id = Utilities.create_rounded_rectangle(
            self, 0, 0, width, height, radius=10, fill=bg, outline=""
        )
        
        self.text_id = self.create_text(width/2, height/2, text=text, fill=fg, font=font)
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_click(self, _):
        self.command()
    
    def on_enter(self, _):
        self.itemconfig(self.rect_id, fill=self.hover_bg)
    
    def on_leave(self, _):
        self.itemconfig(self.rect_id, fill=self.bg)
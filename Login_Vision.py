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

#Para el reconocimiento facial
class FacialRecognitionSystem:
    def _init_(self):
        self.login_attempts = 3
        self.current_user = None
        self.cap = None
        self.root = tk.Tk()
        Utilities.ensure_directories()
        self.login_window = None  

    def run(self):
        self.show_main_screen()
        self.root.mainloop()

    def show_main_screen(self):
        self.root.title("Sistema de Reconocimiento Facial")
        self.root.configure(bg=Config.BG_COLOR)
        Utilities.center_window(self.root, Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        
        self.main_frame = tk.Frame(self.root, bg=Config.BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        header_frame = tk.Frame(self.main_frame, bg=Config.BG_COLOR)
        header_frame.pack(pady=(0, 30))
        
        tk.Label(header_frame, text="Sistema de Reconocimiento Facial", 
                font=Config.TITLE_FONT, bg=Config.BG_COLOR, fg=Config.TEXT_COLOR).pack(pady=(20, 10))
        
        tk.Label(header_frame, text="Inicio de sesión SOLO con reconocimiento facial", 
                font=Config.SUBTITLE_FONT, bg=Config.BG_COLOR, fg=Config.TEXT_COLOR).pack()
        
        self.button_frame = tk.Frame(self.main_frame, bg=Config.BG_COLOR)
        self.button_frame.pack(pady=50)
        
        self.login_button = ModernButton(self.button_frame, "Iniciar Sesión Facial", self.show_login_screen, 
                                        width=300, height=50, bg=Config.PRIMARY_COLOR)
        self.login_button.pack(pady=15)
        
        self.register_button = ModernButton(self.button_frame, "Registrar Usuario Facial", self.show_register_screen, 
                                           width=300, height=50, bg=Config.SECONDARY_COLOR)
        self.register_button.pack(pady=15)

            def show_login_screen(self):
        if self.login_attempts <= 0:
            messagebox.showerror("Bloqueado", "Sistema bloqueado por demasiados intentos fallidos.")
            return
        
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login Facial")
        self.login_window.configure(bg=Config.BG_COLOR)
        Utilities.center_window(self.login_window, 520, 420)
        
        card = tk.Frame(self.login_window, bg=Config.CARD_COLOR, bd=0, relief="flat")
        card.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        tk.Label(card, text="🔐 Iniciar Sesión Facial", 
                font=Config.SUBTITLE_FONT, bg=Config.CARD_COLOR, fg=Config.PRIMARY_COLOR).pack(pady=(10, 20))
        
        tk.Label(card, text="Usuario", font=Config.LABEL_FONT, bg=Config.CARD_COLOR, fg=Config.TEXT_COLOR).pack(anchor="w", pady=(10, 5))
        self.login_user_entry = ttk.Entry(card, width=30, font=("Segoe UI", 11))
        self.login_user_entry.pack(ipady=8, fill=tk.X, pady=5)
        
        ModernButton(card, "Iniciar con Reconocimiento Facial", self.facial_login, 
                    width=280, height=45, bg=Config.PRIMARY_COLOR).pack(pady=30)

    def show_register_screen(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Registro Facial")
        register_window.configure(bg=Config.BG_COLOR)
        Utilities.center_window(register_window, 520, 420)
        
        card = tk.Frame(register_window, bg=Config.CARD_COLOR, bd=0, relief="flat")
        card.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        tk.Label(card, text="📝 Registro de Usuario", 
                font=Config.SUBTITLE_FONT, bg=Config.CARD_COLOR, fg=Config.PRIMARY_COLOR).pack(pady=(10, 20))
        
        tk.Label(card, text="Usuario", font=Config.LABEL_FONT, bg=Config.CARD_COLOR, fg=Config.TEXT_COLOR).pack(anchor="w", pady=(10, 5))
        self.reg_user_entry = ttk.Entry(card, width=30, font=("Segoe UI", 11))
        self.reg_user_entry.pack(ipady=8, fill=tk.X, pady=5)
        
        ModernButton(card, "Registrar Rostro", self.facial_registration, 
                    width=280, height=45, bg=Config.SECONDARY_COLOR).pack(pady=30)
        
def facial_registration(self):
        username = self.reg_user_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Ingrese un usuario antes de registrar")
            return
        
        capture_window = tk.Toplevel(self.root)
        capture_window.title("Registro Facial")
        capture_window.configure(bg=Config.BG_COLOR)
        Utilities.center_window(capture_window, 720, 620)
        
        info = tk.Label(capture_window, text="Asegúrate de que tu rostro esté bien iluminado.\n"
                       "Colócate de frente y presiona 'Capturar'.", 
                       font=Config.LABEL_FONT, bg=Config.BG_COLOR, fg=Config.TEXT_COLOR)
        info.pack(pady=(10, 5))
        
        video_label = tk.Label(capture_window, bg=Config.BG_COLOR)
        video_label.pack()
        
        ModernButton(capture_window, "Capturar", lambda: self.capture_face(username, capture_window), 
                    width=150, height=40).pack(pady=20)
        
        self.start_camera(video_label)
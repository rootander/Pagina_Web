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

class FacialRecognitionSystem:
    def __init__(self):
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

    def start_camera(self, video_label):
        if self.cap is not None:
            self.cap.release()
        
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            messagebox.showerror("Error", "No se pudo abrir o aperturar la cámara.")
            self.cap = None
            return
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
        
        def update_frame():
            if self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.flip(frame, 1)
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.5, fy=0.5)
                    face_locations = face_recognition.face_locations(small_frame, model="hog")
                    
                    scale_factor = 2
                    face_locations = [(top*scale_factor, right*scale_factor, 
                                      bottom*scale_factor, left*scale_factor) 
                                     for (top, right, bottom, left) in face_locations]
                    
                    for top, right, bottom, left in face_locations:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    
                    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    img = img.resize((640, 480), Image.LANCZOS)
                    imgtk = ImageTk.PhotoImage(image=img)
                    video_label.imgtk = imgtk
                    video_label.configure(image=imgtk)
            
            if video_label.winfo_exists():  
                video_label.after(30, update_frame)  # ~33 FPS
        
        update_frame()

    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def capture_face(self, username, window):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.5, fy=0.5)
                face_locations = face_recognition.face_locations(small_frame, model="hog")
                
                if not face_locations:
                    messagebox.showerror("Error", "No se detectó rostro. Intenta nuevamente.")
                    return
                
                scale_factor = 2
                face_locations = [(top*scale_factor, right*scale_factor, 
                                  bottom*scale_factor, left*scale_factor) 
                                 for (top, right, bottom, left) in face_locations]
                
                top, right, bottom, left = face_locations[0]
                
                top = max(0, top); left = max(0, left)
                bottom = min(frame.shape[0], bottom)
                right = min(frame.shape[1], right)
                
                face_image = frame[top:bottom, left:right]
                if face_image.size == 0:
                    messagebox.showerror("Error", "Recorte inválido del rostro. Intenta otra vez.")
                    return
                
                face_image = cv2.resize(face_image, (150, 200))
                save_path = Utilities.usuario_jpg(username)
                cv2.imwrite(save_path, face_image)
                
                # Verificar que el encoding se pueda extraer
                ref_img = face_recognition.load_image_file(save_path)
                encs = face_recognition.face_encodings(ref_img)
                if not encs:
                    os.remove(save_path)
                    messagebox.showerror("Error", "No se pudo procesar el rostro. Vuelve a intentar.")
                    return
                
                messagebox.showinfo("Éxito", "Usuario registrado con éxito")
                window.destroy()
                self.stop_camera()
def facial_login(self):
        if self.login_attempts <= 0:
            messagebox.showerror("Bloqueado", "Sistema bloqueado por demasiados intentos fallidos.")
            return
        
        username = self.login_user_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Ingrese un usuario")
            return
        
        face_path = Utilities.usuario_jpg(username)
        if not os.path.exists(face_path):
            messagebox.showerror("Error", "Usuario no registrado con reconocimiento facial")
            return
        
        try:
            reference_image = face_recognition.load_image_file(face_path)
            reference_encodings = face_recognition.face_encodings(reference_image)
            if not reference_encodings:
                messagebox.showerror("Error", "No se pudo leer el rostro registrado. Registra de nuevo.")
                return
            reference_encoding = reference_encodings[0]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la referencia: {e}")
            return
        
        login_window = tk.Toplevel(self.root)
        login_window.title("Login Facial")
        login_window.configure(bg=Config.BG_COLOR)
        Utilities.center_window(login_window, 740, 720)
        
        header = tk.Label(login_window, text=f"Tienes {Config.LOGIN_DURATION} segundos para autenticarte.\n"
                         f"Cuenta regresiva y resultado en tiempo real.", 
                         font=Config.SUBTITLE_FONT, bg=Config.BG_COLOR, fg=Config.TEXT_COLOR)
        header.pack(pady=(10, 5))
        
        timer_label = tk.Label(login_window, text="", font=Config.LABEL_FONT, bg=Config.BG_COLOR, fg=Config.TEXT_COLOR)
        timer_label.pack(pady=(0, 5))
        
        percent_label = tk.Label(login_window, text="Coincidencia: 0%", font=Config.LABEL_FONT, bg=Config.BG_COLOR, fg=Config.PRIMARY_COLOR)
        percent_label.pack(pady=(0, 10))
        
        video_label = tk.Label(login_window, bg=Config.BG_COLOR)
        video_label.pack()
        
        status_label = tk.Label(login_window, text="Esperando detección...", font=Config.LABEL_FONT, bg=Config.BG_COLOR, fg=Config.TEXT_COLOR)
        status_label.pack(pady=10)
        
        self.start_facial_login(video_label, timer_label, status_label, percent_label, reference_encoding, username, login_window)

def start_facial_login(self, video_label, timer_label, status_label, percent_label, reference_encoding, username, login_window):
        start_time = time.time()
        matches = 0
        total_frames = 0
        
        if self.cap is not None:
            self.cap.release()
        
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            messagebox.showerror("Error", "No se pudo abrir la cámara.")
            return
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
        
        def update_frame():
            nonlocal matches, total_frames
            
            elapsed = time.time() - start_time
            remaining = max(0, Config.LOGIN_DURATION - int(elapsed))
            timer_label.config(text=f"Tiempo restante: {remaining} s")
            
            if elapsed >= Config.LOGIN_DURATION:
                self.stop_camera()
                ratio = (matches / total_frames) if total_frames else 0.0
                
                if ratio >= Config.FACE_MATCH_THRESHOLD:
                    status_label.config(text=f"✓ Reconocimiento exitoso ({ratio:.0%})", fg=Config.SUCCESS_COLOR)
                    if self.login_window and self.login_window.winfo_exists():
                        self.login_window.destroy()
                    login_window.after(1000, lambda: (login_window.destroy(), self.show_dashboard(username)))
                else:
                    self.login_attempts -= 1
                    intentos_msg = f" Intentos restantes: {self.login_attempts}" if self.login_attempts > 0 else ""
                    status_label.config(text=f"✗ Usuario desconocido ({ratio:.0%}).{intentos_msg}", fg=Config.ERROR_COLOR)
                    login_window.after(1500, login_window.destroy)
                    
                    if self.login_attempts <= 0:
                        messagebox.showerror("Bloqueado", "Sistema bloqueado por demasiados intentos fallidos.")
                        self.login_button.unbind("<Button-1>")
                        self.register_button.unbind("<Button-1>")
                        self.login_button.itemconfig(self.login_button.rect_id, fill="#999999")
                        self.register_button.itemconfig(self.register_button.rect_id, fill="#999999")
                        self.login_button.itemconfig(self.login_button.text_id, fill="#666666")
                        self.register_button.itemconfig(self.register_button.text_id, fill="#666666")
                return
            
            if self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.flip(frame, 1)
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.5, fy=0.5)
                    face_locations = face_recognition.face_locations(small_frame, model="hog")
                    
                    scale_factor = 2
                    face_locations = [(top*scale_factor, right*scale_factor, 
                                      bottom*scale_factor, left*scale_factor) 
                                     for (top, right, bottom, left) in face_locations]
                    
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    total_frames += 1
                    any_match = False
                    
                    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                        results = face_recognition.compare_faces(
                            [reference_encoding], face_encoding, tolerance=Config.FACE_TOLERANCE
                        )
                        is_match = bool(results[0]) if results else False
                        any_match |= is_match
                        
                        if is_match:
                            matches += 1
                        
                        color = (0, 255, 0) if is_match else (0, 0, 255)
                        label = username if is_match else "Desconocido"
                        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                        cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                    
                    ratio = (matches / total_frames) if total_frames else 0.0
                    percent_label.config(text=f"Coincidencia: {ratio:.0%}")
                    
                    if any_match:
                        status_label.config(text=f"Rostro reconocido: {username}", fg=Config.SUCCESS_COLOR)
                    else:
                        status_label.config(text="Rostro no coincide", fg=Config.ERROR_COLOR)
                    
                    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    img = img.resize((640, 480), Image.LANCZOS)
                    imgtk = ImageTk.PhotoImage(image=img)
                    video_label.imgtk = imgtk
                    video_label.configure(image=imgtk)
            
            if video_label.winfo_exists():  
                video_label.after(30, update_frame)  
        
        update_frame()

    
def show_dashboard(self, username):
        dashboard = tk.Toplevel(self.root)
        dashboard.title("Dashboard")
        dashboard.configure(bg=Config.BG_COLOR)
        Utilities.center_window(dashboard, 800, 600)
        
        tk.Label(dashboard, text=f"Bienvenido, {username}!", 
                font=Config.TITLE_FONT, bg=Config.BG_COLOR, fg=Config.TEXT_COLOR).pack(pady=20)
        
        tk.Label(dashboard, text=datetime.now().strftime("%d/%m/%Y %H:%M"), 
                font=Config.LABEL_FONT, bg=Config.BG_COLOR, fg=Config.TEXT_COLOR).pack(pady=(0, 20))
        
        ModernButton(dashboard, "Cerrar Sesión", dashboard.destroy, 
                    width=200, height=40, bg=Config.ERROR_COLOR).pack(pady=20)

if __name__ == "__main__":
    app = FacialRecognitionSystem()
    app.run()
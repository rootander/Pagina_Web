import tkinter as tk  # interfaces, ventanas, botones, etiquetas
from tkinter import messagebox, ttk
import os
import cv2  # captura video
import json
import webbrowser
import time
import numpy as np
from PIL import Image, ImageTk
import face_recognition
from api_client import APIClient  # conexión con Spring Boot


# Configuración visual y tamaños
class Config:
    PRIMARY_COLOR = "#6A5ACD"
    SECONDARY_COLOR = "#9370DB"
    BG_COLOR = "#F8F9FA"
    TEXT_COLOR = "#2D3748"
    BUTTON_FONT = ("Segoe UI", 12)
    LABEL_FONT = ("Segoe UI", 11)
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480


class Utilities:
    @staticmethod
    def center_window(window, width, height):
        sw, sh = window.winfo_screenwidth(), window.winfo_screenheight()
        x, y = (sw - width) // 2, (sh - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def usuario_jpg(nombre):
        return f"faces/{nombre}.jpg"

    @staticmethod
    def ensure_directories():
        os.makedirs("faces", exist_ok=True)
        os.makedirs("temp", exist_ok=True)


class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, width=200, height=40,
                 bg=Config.PRIMARY_COLOR, fg="white",
                 font=Config.BUTTON_FONT, hover_bg=Config.SECONDARY_COLOR, *args, **kwargs):
        super().__init__(parent, width=width, height=height,
                         highlightthickness=0, *args, **kwargs)
        self.command = command
        self.bg = bg
        self.hover_bg = hover_bg
        self.rect_id = self.create_rectangle(0, 0, width, height, fill=bg, outline="")
        self.text_id = self.create_text(width // 2, height // 2, text=text, fill=fg, font=font)
        self.bind("<Button-1>", lambda _: self.command())
        self.bind("<Enter>", lambda _: self.itemconfig(self.rect_id, fill=hover_bg))
        self.bind("<Leave>", lambda _: self.itemconfig(self.rect_id, fill=bg))


class FacialRecognitionSystem:
    def __init__(self):
        self.root = tk.Tk()
        Utilities.ensure_directories()
        self.api = APIClient(
            user_base_url="http://localhost:8082/api",
            auth_base_url="http://localhost:8082/auth"
        )
        self.known_encodings = {}
        self.attempts_left = 3
        self.jwt_token = None
        self.load_known_encodings()

    def load_known_encodings(self):
        """Carga usuarios desde backend y decodifica sus encodings"""
        try:
            response = self.api.get_all_users()
            if response:
                for user in response:
                    if user.get("faceEncoding"):
                        encoding_list = json.loads(user["faceEncoding"])
                        encoding_array = np.array(encoding_list)
                        self.known_encodings[user["username"]] = encoding_array
        except Exception as e:
            print(f"[ERROR] No se pudieron cargar encodings: {e}")

    def run(self):
        self.show_main_screen()
        self.root.mainloop()

    def show_main_screen(self):
        self.root.title("Sistema de Reconocimiento Facial")
        self.root.configure(bg=Config.BG_COLOR)
        Utilities.center_window(self.root, Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

        frame = tk.Frame(self.root, bg=Config.BG_COLOR)
        frame.pack(expand=True)

        tk.Label(frame, text="🔐 Login Facial", font=Config.LABEL_FONT,
                 bg=Config.BG_COLOR, fg=Config.TEXT_COLOR).pack(pady=20)

        ModernButton(frame, "Iniciar sesión con rostro",
                     self.video_login_with_visual_feedback, width=300, height=50).pack(pady=15)
        ModernButton(frame, "Registrar Usuario",
                     self.show_register_screen, width=300, height=50).pack(pady=15)

    def show_register_screen(self):
        win = tk.Toplevel(self.root)
        win.title("Registro Usuario Facial")
        Utilities.center_window(win, 500, 400)

        tk.Label(win, text="Usuario", font=Config.LABEL_FONT).pack(pady=10)
        self.reg_user_entry = ttk.Entry(win, width=30)
        self.reg_user_entry.pack(pady=5)
        ModernButton(win, "Registrar Rostro",
                     lambda: self.facial_registration(win),
                     width=250, height=45).pack(pady=30)

    def facial_registration(self, window):
        username = self.reg_user_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Ingrese un nombre de usuario")
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo abrir la cámara")
            return

        preview_win = tk.Toplevel(window)
        preview_win.title("Capturar Rostro")
        Utilities.center_window(preview_win, Config.CAMERA_WIDTH, Config.CAMERA_HEIGHT + 60)
        label_video = tk.Label(preview_win)
        label_video.pack()

        def update_frame():
            ret, frame = cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                label_video.imgtk = imgtk
                label_video.configure(image=imgtk)
            label_video.after(10, update_frame)

        def capture_face():
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "No se pudo capturar la imagen")
                cap.release()
                preview_win.destroy()
                return

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb)
            if not encodings:
                messagebox.showerror("Error", "No se detectó rostro. Intenta de nuevo.")
                return

            encoding_json = json.dumps(encodings[0].tolist())
            img_path = Utilities.usuario_jpg(username)
            cv2.imwrite(img_path, frame)

            response = self.api.create_user(username, f"{username}@example.com", encoding_json)
            if response:
                messagebox.showinfo("Éxito", f"Usuario {username} registrado correctamente.")
                self.known_encodings[username] = encodings[0]
                cap.release()
                preview_win.destroy()
                window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario en el backend.")

        tk.Button(preview_win, text="📸 Capturar Rostro",
                  command=capture_face, bg="#4CAF50", fg="white",
                  font=Config.BUTTON_FONT).pack(pady=10)

        update_frame()

    def video_login_with_visual_feedback(self):
        if self.attempts_left <= 0:
            messagebox.showerror("Sistema bloqueado", "Se agotaron los intentos.")
            self.root.destroy()
            return

        user_win = tk.Toplevel(self.root)
        user_win.title("Login - Ingresar Usuario")
        Utilities.center_window(user_win, 400, 200)

        tk.Label(user_win, text="Ingrese su nombre de usuario:",
                 font=Config.LABEL_FONT).pack(pady=10)
        user_entry = ttk.Entry(user_win, width=30)
        user_entry.pack(pady=5)

        def start_login():
            username = user_entry.get().strip()
            if not username:
                messagebox.showerror("Error", "Debe ingresar un usuario")
                return

            if username not in self.known_encodings:
                messagebox.showerror("Error", f"Usuario '{username}' no existe o no tiene rostro registrado")
                return

            user_win.destroy()
            self.start_camera_login(username)

        ModernButton(user_win, "Iniciar con cámara", start_login,
                     width=250, height=45).pack(pady=20)

    def start_camera_login(self, username):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo abrir la cámara")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Login facial de {username}")
        Utilities.center_window(win, Config.CAMERA_WIDTH, Config.CAMERA_HEIGHT + 100)

        label_video = tk.Label(win)
        label_video.pack()

        label_timer = tk.Label(win, text="Tiempo restante: 10s", font=("Segoe UI", 12), fg="red")
        label_timer.pack(pady=5)

        start_time = time.time()
        user_encoding = self.known_encodings[username]

        def process_frame():
            nonlocal start_time
            ret, frame = cap.read()
            if not ret:
                return

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            recognized = False
            captured_encoding = None

            for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
                match = face_recognition.compare_faces([user_encoding], encoding, tolerance=0.5)[0]
                distance = face_recognition.face_distance([user_encoding], encoding)[0]
                confidence = int((1 - distance) * 100)

                if match:
                    recognized = True
                    captured_encoding = encoding.tolist()
                    color = (0, 255, 0)
                    name_text = f"{username} {confidence}%"
                else:
                    color = (0, 0, 255)
                    name_text = f"Desconocido {confidence}%"

                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name_text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            elapsed = int(time.time() - start_time)
            remaining = max(0, 10 - elapsed)
            label_timer.config(text=f"Tiempo restante: {remaining}s")

            if elapsed >= 10:
                cap.release()
                win.destroy()
                if recognized and captured_encoding is not None:
                    result = self.api.login_with_face(username, captured_encoding)
                    if result and "token" in result:
                       self.jwt_token = result["token"]
                       messagebox.showinfo("Login Exitoso", f"Bienvenido, {username}!")
                # guarda y abre dashboard pasando token en la URL
                       self.root.destroy()
                       webbrowser.open(f"http://localhost:8082/dashboard?token={self.jwt_token}")

                else:
                    self.attempts_left -= 1
                    if self.attempts_left > 0:
                        messagebox.showwarning("Intento fallido", f"No se reconoció el rostro.\nIntentos restantes: {self.attempts_left}")
                    else:
                        messagebox.showerror("Sistema bloqueado", "Se agotaron los intentos.")
                        self.root.destroy()
                return

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            label_video.imgtk = imgtk
            label_video.configure(image=imgtk)
            label_video.after(10, process_frame)

        process_frame()


if __name__ == "__main__":
    app = FacialRecognitionSystem()
    app.run()

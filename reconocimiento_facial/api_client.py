import requests
import json

class APIClient:
    def __init__(self, 
                 user_base_url="http://localhost:8082/api", 
                 auth_base_url="http://localhost:8082/auth"):
        self.user_base_url = user_base_url
        self.auth_base_url = auth_base_url

    
    def create_user(self, username, email, face_encoding, rol="USER"):
       
        if isinstance(face_encoding, list):
            face_encoding = json.dumps(face_encoding)

        data = {
            "username": username,
            "email": email,
            "faceEncoding": face_encoding,
            "rol": rol
        }

        try:
            r = requests.post(f"{self.user_base_url}/usuarios", json=data)
            print(f"[create_user] Status: {r.status_code}, Response: {r.text}")
            return r.status_code in (200, 201)
        except Exception as e:
            print(f"[create_user] Error: {e}")
            return False

    def get_user(self, username):
        try:
            r = requests.get(f"{self.user_base_url}/usuarios/{username}")
            print(f"[get_user] Status: {r.status_code}")
            return r.json() if r.status_code == 200 else None
        except Exception as e:
            print(f"[get_user] Error: {e}")
            return None

    def get_all_users(self):
        try:
            r = requests.get(f"{self.user_base_url}/usuarios")
            print(f"[get_all_users] Status: {r.status_code}")
            return r.json() if r.status_code == 200 else []
        except Exception as e:
            print(f"[get_all_users] Error: {e}")
            return []

    
    def login_with_face(self, username, face_encoding):
       
        if not isinstance(face_encoding, list):
            try:
                face_encoding = face_encoding.tolist()
            except Exception:
                face_encoding = list(face_encoding)

        
        data = {
            "username": username,
            "faceEncoding": face_encoding
        }

        try:
            r = requests.post(
                f"{self.auth_base_url}/login-face",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            print(f"[login_with_face] Status: {r.status_code}, Response: {r.text}")

            if r.status_code == 200:
                return r.json()
            return None
        except Exception as e:
            print(f"[login_with_face] Error: {e}")
            return None

  
    def create_employee(self, usuario_id, nombre, apellido, dni, direccion=None, telefono=None, salario=0.0):
        data = {
            "usuario": {"id": usuario_id},
            "nombre": nombre,
            "apellido": apellido,
            "dni": dni,
            "direccion": direccion,
            "telefono": telefono,
            "salario": salario
        }

        try:
            r = requests.post(f"{self.user_base_url}/empleados", json=data)
            print(f"[create_employee] Status: {r.status_code}, Response: {r.text}")
            return r.json() if r.status_code in (200, 201) else None
        except Exception as e:
            print(f"[create_employee] Error: {e}")
            return None

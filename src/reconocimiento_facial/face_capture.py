import cv2
import face_recognition
import json
import sys
import os

def dibujar_boton(frame):
    
    x, y, w, h = 20, 20, 150, 50
    
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), -1)
    cv2.putText(frame, "Capturar", (x + 10, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    return (x, y, w, h)

def click_en_boton(x, y, boton_coords):
    bx, by, bw, bh = boton_coords
    return bx <= x <= bx + bw and by <= y <= by + bh

def main():
    encoding = None
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara")
        sys.exit(1)

    print("🎥 Haz clic en el botón 'Capturar' para tomar el rostro")

    ventana = "Captura de Rostro"
    cv2.namedWindow(ventana)

    
    captura_realizada = False

    def mouse_callback(event, x, y, flags, param):
        nonlocal captura_realizada
        if event == cv2.EVENT_LBUTTONDOWN:
            if click_en_boton(x, y, param):
                captura_realizada = True

    boton_coords = (20, 20, 150, 50)
    cv2.setMouseCallback(ventana, mouse_callback, boton_coords)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ No se pudo acceder a la cámara")
            break

      
        dibujar_boton(frame)

        cv2.imshow(ventana, frame)

        if captura_realizada:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = face_recognition.face_encodings(rgb_frame)
            if faces:
                encoding = faces[0].tolist()
                print("✅ Rostro capturado")
            else:
                print("⚠ No se detectó rostro")
            break

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  
            print("❌ Cancelado por el usuario")
            encoding = None
            break

    cap.release()
    cv2.destroyAllWindows()


    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "encoding.json")

    data = {"encoding": encoding} if encoding else {"error": "No se detectó rostro"}
    data["log"] = "Script ejecutado"

    try:
        with open(json_path, "w") as f:
            json.dump(data, f)
        print(f"📁 encoding.json guardado en {json_path}")
    except Exception as e:
        print(f"❌ Error al guardar encoding.json: {e}")

if __name__ == "__main__":
    main()

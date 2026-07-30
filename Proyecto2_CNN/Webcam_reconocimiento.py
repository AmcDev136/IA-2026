# Scriopt de reconocimiento facial
# Flujo:
# 1. Haar Cascade detecta la posición (bounding box) de los rostros -> SOLO detección.
# 2. El recorte de cada rostro se preprocesa (gris, 150x150, normalizado).
# 3. La CNN entrenada (modelo_caras.keras) predice la identidad -> clasificación.
# 4. Se dibuja el resultado sobre el frame de la webcam.
# Presiona ESC para salir.

import json
import cv2 as cv
import numpy as np
import tensorflow as tf

# Configuracion
MODEL_PATH = "D:/IA Verano 2026/modelo__caras.keras"
LABELS_PATH = "D:/IA Verano 2026/clases.json"
IMG_SIZE = 150
CONFIDENCE_THRESHOLD = 0.80

# Carga de modelo y etiquetas
print("Cargando modelo CNN...")
model = tf.keras.models.load_model(MODEL_PATH)

with open(LABELS_PATH, "r", encoding="utf-8") as f:
    labels__dict = json.load(f) # {"0": "Persona_1", ...}

print(f"Clases cargadas: {labels__dict}")

# Carga del clasificador haarcascade para detección
# cv.data.haarcascade apunta a la carpeta de opencv donde instala los xml
cascade_path = "D:/IA Verano 2026/haarcascade_frontalface_alt2.xml"
face_cascade = cv.CascadeClassifier(cascade_path)

if face_cascade.empty():
    raise IOError(f"No se pudo cargar el clasificador en: {cascade_path}")

# Funcion de preprocesamiento de un rostro recortado
def preprocess_face(face_gray_crop):
    """
    Recibe un recorte de rostro en escala de grises (tamaño variable, según lo que detecto el haar cascade) y lo transforma en el tensor exacto que espera la CNN.
    Flujo:
    (h, w) = Recorte original en escala grises
    (150, 150) = Tras resize
    (150, 150, 1) = Se añade canal
    (1, 150, 150, 1) = Se añade dimension de batch
"""
    face_resized = cv.resize(face_gray_crop, (IMG_SIZE, IMG_SIZE))
    face_tensor = face_resized.astype("float32").reshape(1, IMG_SIZE, IMG_SIZE, 1)
    return face_tensor

# Inicio de la camara
cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise IOError("No se pudo acceder a la cámara.")

print("Camara iniciada, presiona ESC para salir")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame de la camara")
        break

    # Convertimos el frame completo a escala de grises
    # Haar Cascade trabaja sobre imagenes en gris (es más rápido)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Deteccion de rostros + lista de bounding boxes
    faces = face_cascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    for (x, y, w, h) in faces:
        #recortamos el rostro directamente del frame gris
        face_crop = gray_frame[y:y + h, x:x + w]

        # Preprocesamos para coincidir con la entrada esperada
        input_tensor = preprocess_face(face_crop)

        # Prediccion: vector de posibilidades softmax
        predictions = model.predict(input_tensor, verbose=0)
        predicted_index = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_index])

        if confidence >= CONFIDENCE_THRESHOLD:
            name = labels__dict.get(str(predicted_index), "Desconocido")
            color = (0, 255, 0) 
        else:
            name = "Desconocido"
            color = (0, 0, 255) # rojo, confianza baja

        label_text = f"{name} ({confidence * 100:.1f}%)"

        # Dibujamos el bounding box y texto sobre frame
        cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv.putText(
            frame,
            label_text,
            (x, y - 10 if y - 10 > 10 else y + 20),
            cv.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    cv.imshow("Reconocimiento facial - CNN", frame)

    # ESC para salir
    key = cv.waitKey(1) & 0xFF
    if key == 27:
        print("Cerrando")
        break

# Limpieza de recursos
cap.release()
cv.destroyAllWindows()
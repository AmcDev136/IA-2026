import numpy as np
import cv2 as cv
import os
import time  # necesario para medir el tiempo entre capturas

output_folder = 'D:/Caras/Will_Smith/'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt2.xml')
cap = cv.VideoCapture('D:/Will.mp4')
x = y = w = h = 0
count = 0
img = None

# Control de intervalo de captura
CAPTURE_INTERVAL = 2.0        # segundos entre cada foto guardada
last_capture_time = 0.0       # marca de tiempo de la última foto guardada

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)

    tiempo_actual = time.time()
    # ¿Ya pasó suficiente tiempo desde la última captura guardada?
    puede_capturar = (tiempo_actual - last_capture_time) >= CAPTURE_INTERVAL

    for (x, y, w, h) in rostros:
        img = frame[y:y + h, x:x + w]  # recorte del rostro (a color, tamaño variable)

        # Solo guardamos si ya pasó el intervalo definido
        if puede_capturar:
            # Redimensionamos el recorte a 150x150 antes de guardar, para que
            # coincida con el tamaño esperado por el entrenamiento (train_cnn.py)
            img_guardar = cv.resize(img, (150, 150), interpolation=cv.INTER_CUBIC)

            count += 1
            name = output_folder + 'Will' + str(count) + '.jpg'
            cv.imwrite(name, img_guardar)

            last_capture_time = tiempo_actual
            puede_capturar = False  # evita guardar 2 veces en el mismo frame si hay varios rostros

        m1 = int(h / 2)
        n1 = int(w / 2)
        frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        frame = cv.circle(frame, (x + n1, y + m1), int(w / 2), (255, 0, 0), 2)

    # Texto en pantalla para saber cuánto falta para la siguiente captura
    tiempo_restante = max(0.0, CAPTURE_INTERVAL - (tiempo_actual - last_capture_time))
    cv.putText(frame, f"Fotos guardadas: {count} | Siguiente en: {tiempo_restante:.1f}s",
               (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv.imshow('rostros', frame)

    if img is not None:
        cv.imshow('cara', img)

    k = cv.waitKey(30)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
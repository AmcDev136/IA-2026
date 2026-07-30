import os
import cv2 as cv

# 1. Rutas de carpetas
input_folder = 'D:/Caras/ryan gosling'  # Carpeta donde se guardaron las imágenes descargadas
output_folder = 'D:/Caras/Ryan/'            # Carpeta donde se guardarán los rostros recortados

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 2. Cargar el detector de rostros
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt2.xml')

count = 0
archivos = os.listdir(input_folder)
total_imagenes = len(archivos)

print(f"Se encontraron {total_imagenes} imágenes en '{input_folder}'. Iniciando procesamiento...")

# 3. Recorrer foto por foto
for i, file_name in enumerate(archivos, start=1):
    image_path = os.path.join(input_folder, file_name)
    
    # Leer la imagen
    frame = cv.imread(image_path)
    
    # Si la imagen está corrupta o no es un formato válido, la ignoramos
    if frame is None:
        print(f"[{i}/{total_imagenes}] Error al abrir {file_name}. Se omitirá.")
        continue

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    img_recorte = None

    for (x, y, w, h) in rostros:
        # Recorte del rostro a color
        img_recorte = frame[y:y + h, x:x + w]

        # Redimensionar a 150x150 para el entrenamiento
        img_guardar = cv.resize(img_recorte, (150, 150), interpolation=cv.INTER_CUBIC)

        count += 1
        name = os.path.join(output_folder, f'RyanFaceee{count}.jpg')
        cv.imwrite(name, img_guardar)

        # Dibujar marcas visuales en la imagen original para la vista previa
        m1 = int(h / 2)
        n1 = int(w / 2)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.circle(frame, (x + n1, y + m1), int(w / 2), (255, 0, 0), 2)

    # 4. Mostrar vista previa en pantalla
    cv.putText(frame, f"Foto {i}/{total_imagenes} | Rostros guardados: {count}",
               (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv.imshow('Procesando carpeta...', frame)

    if img_recorte is not None:
        cv.imshow('Último rostro recortado', img_recorte)

    # Espera 100 ms por foto para que puedas ver el avance en pantalla.
    # Presiona ESC si deseas cancelar el proceso antes de terminar.
    k = cv.waitKey(100)
    if k == 27:  # ESC
        print("Proceso cancelado por el usuario.")
        break

cv.destroyAllWindows()
print(f"¡Proceso completado! Se extrajeron {count} rostros y se guardaron en '{output_folder}'.")
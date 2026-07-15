import cv2 as cv
import numpy as np
import os

data_set = "D:/Caras/"
faces = sorted(os.listdir(data_set))
print("Personas:", faces)

labels = []
faces_data = []
label = 0

ancho, alto = 150, 150

for person in faces:
    person_path = os.path.join(data_set, person)
    if not os.path.isdir(person_path):
        continue

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        img = cv.imread(img_path, 0)

        if img is None:
            continue

        #Redimensionar caras
        img_resized = cv.resize(img, (ancho, alto))

        labels.append(label)
        faces_data.append(img_resized)
    print(f"  {person} (label={label}): {labels.count(label)} imágenes")
    label += 1

face_recognizer = cv.face.EigenFaceRecognizer_create()
face_recognizer.train(faces_data, np.array(labels))
face_recognizer.write("Eigenface1.xml")
print("Modelo escrito: Eigenface.xml")
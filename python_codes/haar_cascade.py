import numpy as np
import cv2 as cv
import os

output_folder = 'D:/Caras/Fer/'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt2.xml')
cap = cv.VideoCapture(0)
x=y=w=h= 0 
count = 0
img = None
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in rostros:
        img = frame[y:y+h, x:x+w] # recorte del rostro
        imgr = cv.resize(frame, (100, 100))
        count += 1
        name = output_folder+ 'CarFer' + str(count)+'.jpg'
        cv.imwrite(name, img)

        m1 = int(h/2)
        n1 = int(w/2)
        frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
        frame = cv.circle(frame, (x+n1,y+m1), int(w/2) , (255, 0 ,0), 2 )

    cv.imshow('rostros', frame)

    if img is not None:
        cv.imshow('cara', img)
    
    k = cv.waitKey(30)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while (True):
    ret, img = cap.read()
    if(ret):
        #gris = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img2 = np.zeros((img.shape[:2]), np.uint8 )
        b, g, r = cv.split(img)
        #Efecto espejo
        #espejo = cv.flip(img, 1)

        rojo = cv.merge([r, img2, img2])
        verde = cv.merge([img2, g, img2])
        azul = cv.merge([img2, img2, b])

        cv.imshow('img', img2)
        #cv.imshow('gris', gris)
        #cv.imshow('espejo', espejo)
        #cv.imshow('r', r)
        #cv.imshow('g', g)
        #cv.imshow('b', b)
        cv.imshow('rojo', rojo)
        cv.imshow('verde', verde)
        cv.imshow('azul', azul)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    else:
        print("No se pudo abrir la camara")

cap.release()
cv.destroyAllWindows()
#rotar 30 grados en sentido horario, 60 en antihorario y escalar en 2
import cv2 as cv
import numpy as np
import math

#cargar imagen
img = cv.imread ('D:\IA Verano 2026\Caras\Caras14.jpg', 0)

#obtener tamaño de la imagen
x, y =img.shape[:2]

# Transformacion manual
centro = (y // 2, x // 2)

#Angulo neto
angulo_net = 30
esc = 2

# Generar matriz
matriz = cv.getRotationMatrix2D(centro, angulo_net, esc)

#Calcular nuevo tamaño
new_x = y * esc
new_y = x * esc

#aplcar transformacion
img_trans = cv.warpAffine(img, matriz, (new_x, new_y))

#uso de resize
img_resize = cv.resize(img, (new_x, new_y), interpolation=cv.INTER_LINEAR)

#mostrar imagen original y resultado
cv.imshow('imagen original', img)
cv.imshow('imagen rotada 30deg y escalada x2 (matriz)', img_trans)
cv.imshow('imagen escalada x2 con resize', img_resize)
cv.waitKey(0)
cv.destroyAllWindows
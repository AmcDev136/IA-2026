import cv2 as cv
import numpy as np

#Leer imagen
img = cv.imread('D:\IA Verano 2026\Carros.jpg')

#Convertir la imagen a HSV
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

#Definir el rango inferior y superior para detectar verde
lower_red = np.array([0, 65, 65]) # Hue, saturacion, brillo
upper_red = np.array([10, 255, 255])

lower_red1 = np.array([170, 60, 60])
upper_red1 = np.array([180, 255, 255])

#Crear mascara
mask1 = cv.inRange(hsv, lower_red, upper_red)
mask2 = cv.inRange(hsv, lower_red1, upper_red1)

mask = mask1 + mask2

#Aplicar mascara a la imagen
result = cv.bitwise_and(img, img, mask=mask)

#mostrar imagen original y resultado
cv.imshow('Original', img)
cv.imshow('Res', result)
cv.imshow('Mask', mask)

cv.waitKey(0)
cv.destroyAllWindows()
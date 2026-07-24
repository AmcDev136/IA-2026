import cv2

img = cv2.imread('D:\IA Verano 2026\desc.jpg', 0)
print(img.shape)
# Binarizacion
x,y = img.shape
for i in range(x):
    for j in range(y):
        if (img[i, j] < 155):
            img[i, j] = 0
        else:
            img[i, j] = 255

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2 as cv
import os

data_set = "D:/Caras/"
faces = sorted(
    d for d in os.listdir(data_set)
    if os.path.isdir(os.path.join(data_set, d))
)

face_recognizer = cv.face.EigenFaceRecognizer_create()
face_recognizer.read("Eigenface1.xml")

cap = cv.VideoCapture(0)
cascade = cv.CascadeClassifier("haarcascade_frontalface_alt2.xml")
THRESHOLD = 2800  # bajar = más estricto

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = cascade.detectMultiScale(gray, 1.3, 3)

    for (x, y, w, h) in rostros:
        roi = cv.resize(gray[y:y + h, x:x + w], (150, 150),
                        interpolation=cv.INTER_CUBIC)
        label_id, confidence = face_recognizer.predict(roi)

        if confidence < THRESHOLD:
            name = faces[label_id]
            color = (0, 255, 0)
            text = f"{name} ({confidence:.0f})"
        else:
            color = (0, 0, 255)
            text = f"Desconocido ({confidence:.0f})"

        cv.putText(frame, text, (x, y - 12), cv.FONT_HERSHEY_SIMPLEX, 0.7, color, 1, cv.LINE_AA)
        cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    cv.imshow("Eigenfaces", frame)
    if cv.waitKey(1) == 27:  # ESC
        break

cap.release()
cv.destroyAllWindows()
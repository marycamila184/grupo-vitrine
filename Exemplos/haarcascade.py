from __future__ import print_function
import cv2 as cv

def detectAndDisplay(frame):
    face_cascade = cv.CascadeClassifier('models/haarcascades/haarcascade_frontalface_default.xml')
    eyes_cascade = cv.CascadeClassifier('models/haarcascades/haarcascade_eye.xml')

    # -- Detect faces
    faces = face_cascade.detectMultiScale(frame, minNeighbors=20, minSize=(30, 30), maxSize=(300, 300))

    eyes = eyes_cascade.detectMultiScale(frame, minNeighbors=20, minSize=(10, 10), maxSize=(90, 90))

    for (x, y, w, h) in faces:
        frame = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    for (x, y, w, h) in eyes:
        frame = cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv.imshow('Detecção de Faces - HaarCascade', frame)

cap = cv.VideoCapture(0)

if not cap.isOpened:
    print('--(!) Erro abrindo a camera!')
    exit(0)

while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) Sem captura!')
        break
    detectAndDisplay(frame)
    if cv.waitKey(10) == 27:
        break

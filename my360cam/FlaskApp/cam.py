import urllib
import numpy as np
import cv2

print cv2.__version__

opencvDatapath = "/home/comx-admin/my360camera/my360cam/FlaskApp/opencvdata/haarcascades/"
detector = cv2.CascadeClassifier(opencvDatapath + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture("rtsp://admin:admin12345@192.168.0.199:554/Streaming/channels/2/") #to stream mobile camera with login password

while(True):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break    
cap.release()
cv2.destroyAllWindows()

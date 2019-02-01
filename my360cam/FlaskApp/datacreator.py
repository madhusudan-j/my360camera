import numpy as np
import cv2

opencvDatapath = "/home/comx-admin/my360camera/my360cam/FlaskApp/opencvdata/haarcascades/"
detector= cv2.CascadeClassifier( opencvDatapath + 'haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

id = raw_input('enter user id : ')
samplenum = 0

while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        samplenum = samplenum + 1
        cv2.imwrite("dataset/User."+str(id)+"."+str(samplenum)+".jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.waitKey(100)
    cv2.imshow('face',img)
    cv2.waitKey(1)
    if samplenum > 20:
        break    
cam.release()
cv2.destroyAllWindows()

import cv2
import threading

opencvDatapath = "/home/comx-admin/my360camera/FlaskApp/opencvdata/haarcascades/"

class RecordingThread (threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    def __init__(self, camera_ip = 0):
        # Open a camera
        self.cap = cv2.VideoCapture(camera_ip)
      
        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        ret, frame = self.cap.read()
        detector= cv2.CascadeClassifier(opencvDatapath + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        else:
            return None

    def get_frame_detetedface(self):
        detected_faces = set()
        ret, frame = self.cap.read()
        detector= cv2.CascadeClassifier(opencvDatapath + 'haarcascade_frontalface_default.xml')
        rec = cv2.face.LBPHFaceRecognizer_create()
        rec.read("recognizer/trainingdata.yml")
        id = 0 
        font = cv2.FONT_HERSHEY_SIMPLEX  
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            id, conf = rec.predict(gray[y:y+h, x:x+w])
            if id == 1 or id == 11:
                id = "madhu"
                detected_faces.add(id)
            elif id == 222:
                id = "Supreeth"
                detected_faces.add(id)
            elif id == 6:
                id = "sagar"
                detected_faces.add(id)
            else:
                id = "unknown"
                detected_faces.add(id)
            cv2.putText(frame,str(id), (x,y+h),font, 2, 255)
        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        else:
            return None

    def get_detetedfaces(self):
        detected_faces = set()
        ret, frame = self.cap.read()
        detector= cv2.CascadeClassifier(opencvDatapath + 'haarcascade_frontalface_default.xml')
        rec = cv2.face.LBPHFaceRecognizer_create()
        rec.read("recognizer/trainingdata.yml")
        id = 0 
        font = cv2.FONT_HERSHEY_SIMPLEX  
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            id, conf = rec.predict(gray[y:y+h, x:x+w])
            if id == 1:
                id = "madhu"
                detected_faces.add(id)
            elif id == 5:
                id = "gopal"
                detected_faces.add(id)
            elif id == 6:
                id = "sagar"
                detected_faces.add(id)
            else:
                id = "unknown"
                detected_faces.add(id)
            cv2.putText(frame,str(id), (x,y+h),font, 2, 255)
            print(detected_faces)
        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            return detected_faces
        else:
            return None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

    def data_creator(self, user_id):
        user_id = user_id
        no_of_pics = 0
        while(True):
            ret, frame = self.cap.read() # ret, img = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                no_of_pics = no_of_pics + 1
                cv2.imwrite("dataset/User."+str(user_id)+"."+str(no_of_pics)+".jpg", gray[y:y+h, x:x+w])
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                # cv2.waitKey(100)
            # cv2.imshow('face',frame)
            # cv2.waitKey(1)
            if no_of_pics > 20:
                break    
            if ret:
                ret, jpeg = cv2.imencode('.jpg', frame)
                return jpeg.tobytes()
            else:
                return None


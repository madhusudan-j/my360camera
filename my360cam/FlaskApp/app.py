
from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
import cv2

app = Flask(__name__)

video_camera = None
global_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_data', methods=['POST'])
def create_data():
    return Response(data_creator_stream(request = request), mimetype='multipart/x-mixed-replace; boundary=frame')

def data_creator_stream(request):
    user_id = request.form["user_id"]
    print(user_id, "*" * 20)
    user_id = int(user_id)
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.data_creator(user_id)

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')



@app.route('/camera_stream', methods=['POST'])
def camera_stream():
    data = video_details(request = request)
    print(type(data))
    return render_template('camera_stream.html', data = data)

def video_details(request):
    camera_ip = request.form["camera_ip"]
    camera_ip = int(camera_ip)
    print(int(camera_ip), "#" * 20)
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera(camera_ip)
        
    while True:
        frame = video_camera.get_detetedfaces()

        if frame != None:
            global_frame = frame
            data = list(global_frame)
            return data
        else:
            return None

@app.route('/get_user_details')
def get_user_details():
    return video_details(request = request)

@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame_detetedface()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded = True, debug = True)

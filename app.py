from flask import Flask, render_template, Response
from camera import VideoCamera

app = Flask(__name__, static_folder='static')

@app.route('/')
def landing():
    return 'Hello world'

@app.route('/static/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/dynamic/')
def dynamic():
    return render_template('dynamicindex.html')
    
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

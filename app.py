from flask import Flask, render_template, Response, url_for, redirect, session
#from camera import VideoCamera
from authlib.integrations.flask_client import OAuth
import json 

from auth_decorator import login_required

app = Flask(__name__, static_folder='static')
app.secret_key = 'staticdynamicsecretkey'

#oauth config
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='219352619149-adrhc1mhi5trdbik3e2kkrfqaobsjnn6.apps.googleusercontent.com',
    client_secret='H0-7EOHDrX4Zuf8bnz_qK-tf',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/protected')
def protected():
    return 'Logged In'


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    # do something with the token and profile
    session['email'] = user_info['email']
    return redirect('/static')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


@app.route('/static/')
def staticpage():
    return render_template('static.html')

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

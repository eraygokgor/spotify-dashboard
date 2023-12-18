from flask import Flask, redirect, request, make_response
from credentials import CLIENT_ID, CLIENT_SECRET
import requests
import random
import string
import base64 as b64

client_id = CLIENT_ID
client_secret = CLIENT_SECRET
redirect_uri = 'http://127.0.0.1:5000/callback'


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return 'Welcome to Spotify API!'


@app.route('/login')
def authorize():
    print('login request received')
    scope = 'user-read-private user-read-email'
    state_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))

    authorize_url = 'https://accounts.spotify.com/authorize?'
    parameters = 'response_type=code&' + \
                 f'client_id={client_id}&' + \
                 f'scope={scope}&' + \
                 f'redirect_uri={redirect_uri}&' + \
                 f'state={state_key}'

    response = make_response(redirect(authorize_url + parameters))
    return response


@app.route('/callback')
def callback():
    print('callback request received')
    print('---', request.args.get('state'))
    if request.args.get('state') is None:
        print('state is None')
        return redirect('/')
    else:
        url = 'https://accounts.spotify.com/api/token'
        code = request.args.get('code')
        parameters = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri
        }
        headers = {
            'content_type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + b64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')
        }

        response = requests.post(url, data=parameters, headers=headers)
    return response.text

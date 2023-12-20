from flask import Flask, redirect, request
from urllib.parse import urlencode
from credentials import CLIENT_ID, CLIENT_SECRET
from functions import generate_random_string, base64_encoder, sha256_hash
import requests

# Spotify API credentials
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
redirect_uri = 'http://127.0.0.1:5000/callback'

# Spotify API endpoints
SPOTIFY_API_URL = 'https://api.spotify.com/v1/'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Scopes required by your application
SPOTIFY_SCOPES = ['user-read-private', 'user-read-email']

# Local storage
local_storage = dict()

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return 'Welcome to Spotify API!'


@app.route('/login')
def authorize():
    code_verifier = generate_random_string(64)
    # Store the code verifier in local storage to use later to exchange for a token
    local_storage['code_verifier'] = code_verifier
    code_challenge = base64_encoder(sha256_hash(code_verifier))

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': ' '.join(SPOTIFY_SCOPES),
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge,
    }

    auth_url = f'{SPOTIFY_AUTH_URL}?{urlencode(params)}'
    return redirect(auth_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')

    if request.args.get('error'):
        return request.args.get('error')
    else:
        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'code_verifier': local_storage['code_verifier'], # Retrieve the code verifier from local storage
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.post(SPOTIFY_TOKEN_URL, data=params, headers=headers)
        access_token_data = response.json()

        headers_user = {
            'Authorization': f'Bearer {access_token_data["access_token"]}'
        }
        response_user = requests.get(SPOTIFY_API_URL + 'me', headers=headers_user)
        user_data = response_user.json()

        return user_data

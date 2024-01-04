from flask import Flask, redirect, request, render_template, session
from urllib.parse import urlencode
from functions import generate_random_string, base64_encoder, sha256_hash
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Spotify API credentials
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_uri = os.environ.get("REDIRECT_URI")

# Spotify API endpoints
SPOTIFY_API_URL = 'https://api.spotify.com/v1/'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Scopes required by your application
SPOTIFY_SCOPES = ['user-read-private', 'user-read-email', 'user-top-read', 'user-follow-read',
                  'user-read-recently-played', 'user-library-read']

app = Flask(__name__, static_folder='./templates/static', template_folder='./templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
@app.route('/index')
def index():
    print("-----", client_id)
    return render_template('html/index.html')


@app.route('/login')
def authorize():
    code_verifier = generate_random_string(64)
    # Store the code verifier in local storage to use later to exchange for a token
    session['code_verifier'] = code_verifier
    code_challenge = base64_encoder(sha256_hash(code_verifier))

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': ' '.join(SPOTIFY_SCOPES),
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge
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
            'code_verifier': session['code_verifier']  # Retrieve the code verifier from local storage
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.post(SPOTIFY_TOKEN_URL, data=params, headers=headers)
        session['access_token_data'] = response.json()
        return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    access_token = session['access_token_data'].get('access_token')

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    # Get Current User's Profile
    response = requests.get(SPOTIFY_API_URL + 'me', headers=headers)
    user_data = response.json()

    # Get User's Recently Played Tracks
    params = {
        'limit': 50,
    }
    response = requests.get(SPOTIFY_API_URL + 'me/player/recently-played', headers=headers, params=params)
    recently_played = response.json()

    # Get Followed Artists
    params = {
        'limit': 50,
        'type': 'artist'
    }
    response = requests.get(SPOTIFY_API_URL + 'me/following', headers=headers, params=params)
    followed_artists = response.json()

    # Get Saved Albums
    params = {
        'limit': 50,
        # 'market': user_data['country']
    }
    response = requests.get(SPOTIFY_API_URL + 'me/albums', headers=headers, params=params)
    saved_albums = response.json()

    # Get a User's Top Artists
    top_artists = {}
    for term in ['short_term', 'medium_term', 'long_term']:
        params = {
            'time_range': term,  # 'long_term', 'medium_term', 'short_term'
            'limit': 50,
        }
        response = requests.get(SPOTIFY_API_URL + 'me/top/artists', headers=headers, params=params)
        top_artists[term] = response.json()

    # Get a User's Top Tracks
    top_tracks = {}
    for term in ['short_term', 'medium_term', 'long_term']:
        params = {
            'time_range': 'medium_term',  # 'long_term', 'medium_term', 'short_term'
            'limit': 50,
        }
        response = requests.get(SPOTIFY_API_URL + 'me/top/tracks', headers=headers, params=params)
        top_tracks[term] = response.json()

    return render_template('html/dashboard.html',
                           user_data=user_data,
                           followed_artists=followed_artists,
                           recently_played=recently_played,
                           saved_albums=saved_albums,
                           top_artists=top_artists,
                           top_tracks=top_tracks)

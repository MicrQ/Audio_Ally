#!/usr/bin/python3
""" The Flask App and all routes """

from flask import Flask, render_template, request, redirect, url_for, session
import urllib.parse
import requests
from datetime import datetime


app = Flask(__name__)
app.url_map.strict_slashes = False
app.secret_key = 'secret-1234-kkey'

CLIENT_ID = "002dab3c377244fbbaeced9daa4dec45"
CLIENT_SECRET = "4bb022f0ad834a28970b7410b6840bc7"

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_URL = 'https://api.spotify.com/v1/'
REDIRECT_URI ='https://audio-ally.vercel.app/callback'


playlist_data = {}


@app.route('/')
@app.route('/home')
def index():
    """ the main page """
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    playlist_data['genres'] = request.form.getlist('genre')
    playlist_data['playlist_name'] = request.form.get('playlist_name')
    playlist_data['artist'] = request.form.get('fav-artist')
    playlist_data['country'] = request.form.get('country-selector')

    scope = "user-read-private user-read-email playlist-modify-public playlist-modify-private"

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': scope
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return render_template('result.html',
                               message="Error: " + request.args.get('error'))

    if 'code' in request.args:
        req_body = {
            'code': request.args.get('code'),
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info.get('access_token')

        return redirect(url_for('create_playlist'))
    return render_template('result.html',
                           message="Failed to login with Spotify!")
    

@app.route('/create_playlist')
def create_playlist():
    """ a route used to create a playlist with the given data """
    genres = playlist_data['genres']
    artist = playlist_data['artist']
    country = playlist_data['country']

    headers = {
        'Authorization': f'Bearer {session["access_token"]}',
        'Content-Type': 'application/json'
    }

    playlits_json = {
        'name': playlist_data['playlist_name'],
        'public': True
    }

    res = requests.post(API_URL + 'me/playlists',
                        json=playlits_json, headers=headers)
    if res.status_code != 201:
        return render_template('result.html', message=res.text)

    return render_template('result.html',
                           playlist_link=res.json()['external_urls']['spotify'])


@app.route('/contact_us', methods=['GET'])
def contact_us():
    """ route for contact us page """
    return render_template('contact.html')


@app.route('/about', methods=['GET'])
def about():
    """ route for about page """
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)

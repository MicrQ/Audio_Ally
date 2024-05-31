#!/usr/bin/python3
""" The Flask App and all routes """

from flask import Flask, render_template, request
from api_connection import create_connection
from operations import createPlaylist

app = Flask(__name__)
app.url_map.strict_slashes = False


sp = create_connection()


@app.route('/')
@app.route('/home', methods=['GET'])
def index():
    """ the main page """
    return render_template('index.html')


@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    """ a route used to create a playlist with the given data """
    genres = request.form.getlist('genre')
    playlist_name = request.form.get('playlist_name')
    artist = request.form.get('fav-artist')
    country = request.form.get('country-selector')

    if len(genres) == 0 and len(artist) == 0:
        return "<p> you need to select at least one genre or enter artist name </p>"

    if playlist_name == '':
        return "<p> playlist name must be given </p>"


    playlist_link = createPlaylist(sp, playlist_name, genres, artist, country)
    if playlist_link is None:
        return "<h3>invalid option selected</h3>"
    return "<p>link to your playlist <a href='{}'>here</a></p>".format(playlist_link)


@app.route('/contact_us', methods=['GET'])
def contact_us():
    """ route for contact us page """
    return render_template('contact.html')


@app.route('/about', methods=['GET'])
def about():
    """ route for about page """
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True, port='5002')

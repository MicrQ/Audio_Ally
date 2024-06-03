""" Connection with the Spotify API created here """
from os import getenv
from spotipy import Spotify
from spotipy import SpotifyOAuth


def create_connection():
    """
        Creates a connection to the Spotify API using
        the provided client ID and client secret.

        Returns:
            Spotify: A Spotify object representing the connection to the API.
            None: If the client ID or client secret is missing.
    """
    client_id = '2840ca3775034b2b9bc3630cb3b492a2'
    client_secret = '3749d7467e5b42afaddaec1576b863bb'
    scope = 'playlist-modify-public'

    if client_id is None or client_secret is None:
        print('client id or client secret missing')

    auth = SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        scope=scope,
                        redirect_uri="https://audio-ally.vercel.app/callback")
    # print(auth)
    sp = Spotify(auth_manager=auth)
    # print(sp)
    return sp

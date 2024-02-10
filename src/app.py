from __future__ import annotations

from urllib.parse import urlparse

import requests
from fastapi import FastAPI
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from utils import RequestData
from utils import SpotifyPlaylistModel
from utils import UtilityClass
from ytmusicapi import YTMusic
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
ytmusic = YTMusic('oauth.json')


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/spotify_playlist/{playlist_url}')
def get_spotify_playlist_data(playlist_url: str):
    '''This api takes the spotify playlist id and
    returns the json data of all the songs in that playlist'''
    utilities = UtilityClass()
    session_auth_token = utilities.request_access_token()['access_token']
    headers = {
        'Authorization': 'Bearer ' + session_auth_token,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    playlist_id = urlparse(playlist_url).path.split(
        '/',
    )[-1]  # Get's the Playlist ID from URL
    playlist_data = requests.request(
        'GET', f'https://api.spotify.com/v1/playlists/{playlist_id}',
        headers=headers,
    ).json()
    music = {}
    for _ in playlist_data['tracks']['items']:
        music[_['track']['name']] = _['track']['artists'][0]['name']

    return music


@app.post('/ytmusic/create_playlist', status_code=status.HTTP_201_CREATED)
def create_playlist_with_songs(playlist_data: SpotifyPlaylistModel, request_data: RequestData):
    '''This API takes the playlist data collected from /spotify_playlist/{playlist_id} GET method
    and creates a playlist with all songs in Youtube Music'''

    playlist_id = YTMusic.create_playlist(
        self=ytmusic,
        description=request_data['playlist_description'],
        title=request_data['playlist_name'],
        privacy_status=request_data['privacy_status'],
    )
    for song_name, artist_name in playlist_data.items():
        music_info = ytmusic.search(query=song_name + ' by ' + artist_name)
        YTMusic.add_playlist_items(
            self=ytmusic, playlistId=playlist_id, videoIds=[
                music_info[0]['videoId'],
            ],
        )

    return {
        'playlist_name': request_data['playlist_name'],
        'url': f'https://music.youtube.com/playlist?list={playlist_id}',
    }


@app.post('/create_playlist_for_you')
def create_playlist(request_data: RequestData):
    '''This endpoint get the songs and it's respective artists dictionary and creates a playlist in YTMusic'''
    data = get_spotify_playlist_data(request_data['spotify_playlist_url'])
    create_playlist_with_songs(data)

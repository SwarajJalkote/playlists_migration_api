from __future__ import annotations

import os

import requests
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class SpotifyPlaylistModel(BaseModel):
    song_name: str
    artist_name: str


class RequestData(BaseModel):
    spotify_playlist_url: str
    playlist_name: str  # can we removed and fetched from response
    playlist_description: str
    privacy_status: str = 'PRIVATE'


class UtilityClass:
    def __init__(self) -> None:
        '''REFACTORING NEEDED: Hardcoded the creds for now'''
        self.client_id = os.environ['CLIENT_ID']
        self.__client_secret = os.environ['CLIENT_SECRET']

    def request_access_token(self) -> dict:
        payload = {
            'client_id': self.client_id,
            'client_secret': self.__client_secret,
            'grant_type': 'client_credentials',
        }
        access_token = requests.request(
            method='POST',
            url='https://accounts.spotify.com/api/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=payload,
        )

        return access_token.json()

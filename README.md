# playlists_migration_api
APIs to migrate playlists between subscription based music applications such as Youtube Music, Spotify, Amazon Music (TBD)

###### Development:
```python
uvicorn src/app:app --reload
```
###### Production:
```python
uvicorn src/app:app
```
## [OAuth Authentication in YTMusic](https://ytmusicapi.readthedocs.io/en/stable/setup/oauth.html):
```python
pip install ytmusicapi
```
Perform in Terminal:
```python
ytmusicapi oauth
```
and follow the instructions. This will create a file oauth.json in the current directory.

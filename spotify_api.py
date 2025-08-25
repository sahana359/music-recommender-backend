import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")


def search_track(song_name, artist_name=None):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    query = f"track:{song_name}"
    if artist_name:
        query += f" artist:{artist_name}"

    url = "https://api.spotify.com/v1/search"
    params = {"q": query, "type": "track", "limit": 1}
    response = requests.get(url, headers=headers, params=params)

    items = response.json().get("tracks", {}).get("items", [])
    if not items:
        return None

    track = items[0]
    return {
        "track_name": track["name"],
        "artist": track["artists"][0]["name"],
        "album": track["album"]["name"],
        "preview_url": track["preview_url"],
        "album_image": track["album"]["images"][0]["url"]
    }

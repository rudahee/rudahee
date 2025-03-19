import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import os

# Autenticación con las credenciales de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))
# Obtener la canción que estás escuchando
track = sp.current_playback()

if track is not None and track["item"] is not None:
    track_name = track["item"]["name"]
    track_url = track["item"]["external_urls"]["spotify"]
    track_image = track["item"]["album"]["images"][0]["url"]

    # Guardar los resultados en un archivo JSON
    track_data = {
        "track_name": track_name,
        "track_url": track_url,
        "track_image": track_image
    }

    with open("track_data.json", "w") as f:
        json.dump(track_data, f)

else:
    print("No track is currently playing.")

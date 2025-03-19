import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os

# Autenticación OAuth para acceder a la cuenta del usuario (requiere redirección en un entorno local o en producción)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri="http://localhost:8888/callback",
    scope=["user-library-read", "user-read-playback-state", "user-read-currently-playing", "playlist-read-private"]
))

def get_current_track():
    try:
        # Intenta obtener la canción que se está reproduciendo actualmente
        current_track = sp.current_playback()
        if current_track is not None and current_track['item'] is not None:
            track_name = current_track['item']['name']
            track_url = current_track['item']['external_urls']['spotify']
            track_image = current_track['item']['album']['images'][0]['url']
            return {
                "track_name": track_name,
                "track_url": track_url,
                "track_image": track_image
            }
        else:
            return None
    except Exception as e:
        print(f"Error al obtener la canción actual: {e}")
        return None

def get_playlist_track(playlist_id):
    try:
        # Obtiene las canciones de una lista de reproducción
        results = sp.playlist_tracks(playlist_id, limit=1)
        track = results['items'][0]['track']
        track_name = track['name']
        track_url = track['external_urls']['spotify']
        track_image = track['album']['images'][0]['url']
        return {
            "track_name": track_name,
            "track_url": track_url,
            "track_image": track_image
        }
    except Exception as e:
        print(f"Error al obtener la canción de la lista de reproducción: {e}")
        return None

# Intenta obtener la canción actual, y si no está disponible, obtiene una canción de la lista de reproducción
track_data = get_current_track()

if track_data is None:
    # Si no hay una canción en reproducción, obtiene la canción de una lista de reproducción específica
    # Reemplaza 'tu_playlist_id' con el ID de tu lista de reproducción
    playlist_id = "tu_playlist_id"
    track_data = get_playlist_track(playlist_id)

# Guarda los datos en un archivo JSON
with open("track_data.json", "w") as f:
    json.dump(track_data, f)

# Mostrar el track para verificar
print(f"Track: {track_data['track_name']}")
print(f"URL: {track_data['track_url']}")
print(f"Image URL: {track_data['track_image']}")

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
spotify_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{spotify_date}/")
response_text = response.text
soup = BeautifulSoup(response_text,"html.parser")
top_songs = soup.select(selector="li h3",class_ = "c-title")

songs_list = [song.getText().strip() for song in top_songs]
client_id = "79a80aee3b864664a6c04e38bb40bd43"
client_secret = "36144a771a9f49a49a987be2ca75c04f"
URL_REDIRECT = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = spotify_date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

    except IndexError:
        print(f"{song} doesn't exist in spotify. Skipped")

playlist = sp.user_playlist_create(user=user_id,name=f"{spotify_date} Billboard 100",public=False,collaborative=False,description="Spotify playlist to transcend you back in time!")

playlist_song = sp.user_playlist_add_tracks(user=user_id,playlist_id=playlist['id'],tracks=song_uris,position=None)

import json

import spotify
import spotipy
import webbrowser

with open('source.json') as file:
    source = json.load(file)
    username = source['spotify'][0]['username']
    clientID = source['spotify'][0]['clientID']
    clientSecret = source['spotify'][0]['clientSecret']
    redirect_url = source['spotify'][0]['redirect_url']

oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_url)
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user_name = spotifyObject.current_user()


async def ssearch(ctx, *url):
    search = ""
    for i in url:
        search = str(search) + i + " "
    search_song = search
    results = spotifyObject.search(search_song, 1, 0, "track")
    songs_dict = results['tracks']
    song_items = songs_dict['items']
    song = song_items[0]['external_urls']['spotify']
    await ctx.send("Ссылка на песню Spotify: " + song)



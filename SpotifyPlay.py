import json

import discord
import ffmpeg
import spotipy
from spotipy import SpotifyClientCredentials, SpotifyOAuth
import asyncio
import subprocess

import Play

with open('source.json') as file:
    source = json.load(file)
    ffpeg_path = source['files_path'][0]['FFmpegPCMAudio']
    username = source['spotify'][0]['username']
    clientID = source['spotify'][0]['clientID']
    clientSecret = source['spotify'][0]['clientSecret']
    redirect_url = source['spotify'][0]['redirect_url']

oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_url)
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user_name = spotifyObject.current_user()

sp = spotipy.Spotify(auth_manager=oauth_object)

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}


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


async def splay(ctx, *name):
    voice_channel = ctx.guild.voice_client
    if voice_channel is None:
        vc = await ctx.message.author.voice.channel.connect()
        await choose(ctx, vc, *name)
    else:
        if ctx.guild.voice_client.channel == ctx.message.author.voice.channel:
            vc = voice_channel
            await choose(ctx, vc, *name)
        else:
            await ctx.send('Бот находится в другом канале')


async def search_url(ctx, url, vc):
    new_song = url.split("/")[-1]
    track_id = new_song
    track_metadata = sp.track(track_id)
    # получение ссылки на аудиофайл
    audio_url = track_metadata['name']
    await Play.search_name(ctx, audio_url, vc)
    #vc.play(discord.FFmpegPCMAudio(executable=ffpeg_path, source=audio_url, **FFMPEG_OPTIONS))
    #await ctx.send("Проигрываю песню: " + " " + "(" + url + ")")


async def search_name(ctx, name, vc):
    try:
        search_song = name
        results = spotifyObject.search(search_song, 1, 0, "track")
        songs_dict = results['tracks']
        song_items = songs_dict['items']
        song = song_items[0]['external_urls']['spotify']
        await search_url(ctx, song, vc)
    except:
        await ctx.send("По вашему запросу ничего не найдено")
        return


async def choose(ctx, vc, *name):
    if vc.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, очередь в разработке')
        return
    else:
        if "." and "/" in name[0]:
            await search_url(ctx, name[0], vc)
        else:
            search = ""
            for i in name:
                search = str(search) + i + " "
            print(search)
            await search_name(ctx, search, vc)

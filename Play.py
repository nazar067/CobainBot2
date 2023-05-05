import os

import discord
import yt_dlp as youtube_dl
import json

from asyncio import sleep
from youtube_search import YoutubeSearch
from . import utils

# from youtube_dl import YoutubeDL

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -bufsize 16M'
}
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'default_search': 'auto',
    'noplaylist': 'True',
    'simulate': 'True',
    'preferredquality': '192',
    'preferredcodec': 'mp3',
    'key': 'FFmpegExtractAudio'
}
with open('source.json') as file:
    source = json.load(file)
    ffpeg_path = source['files_path'][0]['FFmpegPCMAudio']


async def play(ctx, *name):
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
    try:
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        await ctx.send("По вашему запросу ничего не найдено")
        #await ctx.send(e)
        return
    Url = info['url']

    # SponsorBlock integration
    ffmpeg_options = FFMPEG_OPTIONS.copy()
    segments = utils.get_skip_segments(info.get('id'))

    if segments is not None:
        if ffmpeg_options.get('options') is None:
            ffmpeg_options['options'] = ''
        else:
            ffmpeg_options['options'] += ' '

        opts = utils.get_ffmpeg_sponsor_filter(segments, info.get('duration'))
        ffmpeg_options['options'] += opts


    vc.play(discord.FFmpegPCMAudio(executable=ffpeg_path, source=Url, **ffmpeg_options))
    await ctx.send("Проигрываю видео: " + info.get('title', None) + " " + "(" + url + ")")
    while vc.is_playing():
        await sleep(1)


async def search_name(ctx, name, vc):
    yt = YoutubeSearch(name, max_results=1).to_json()
    try:
        yt_id = str(json.loads(yt)['videos'][0]['id'])
        yt_url = 'https://www.youtube.com/watch?v=' + yt_id
        await search_url(ctx, yt_url, vc)
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

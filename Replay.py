import asyncio

import discord
import yt_dlp as youtube_dl
import json

from asyncio import sleep
from youtube_search import YoutubeSearch

# from youtube_dl import YoutubeDL

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
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

is_running = {}


async def stop_replay(ctx, bot):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await ctx.send("Остнавливаю зацикливание")
    else:
        await ctx.send("Сейчас ничего не проигрывается")
    global is_running
    server_id = str(ctx.guild.id)
    is_running[server_id] = False
    if voice.is_playing():
        voice.stop()


async def replay(ctx, *name):
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
            return


async def search_url(ctx, url, vc):
    global is_running
    server_id = str(ctx.guild.id)
    is_running[server_id] = True
    try:
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    except:
        #await ctx.send("По вашему запросу ничего не найдено")
        return
    Url = info['url']
    await ctx.send("Проигрываю видео: " + info.get('title', None) + " " + "(" + url + ")")
    while True:
        if server_id in is_running and not is_running[server_id]:
            break
        vc.play(discord.FFmpegPCMAudio(executable=ffpeg_path, source=Url, **FFMPEG_OPTIONS))
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()
        await asyncio.sleep(1)


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

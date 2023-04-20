import asyncio

import discord
import json

import openai
import youtube_dl
from discord.ext import commands

import ChatGPT
import DevCommands
import Play
import Replay
import SpotifyPlay
import SteamCommands
import SupportCommands
import TrollCommands

with open('source.json') as file:
    source = json.load(file)
    key = source['token'][0]['key']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)


@bot.event
async def on_ready():
    print("Cobain comeback")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Integration with ChatGPT"))


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title='Команда на задержке.',
            description=f'Повторить через {error.retry_after :.0f} секунд',
            colour=discord.Color.red()
        )

        return await ctx.send(embed=embed)


@bot.event
async def on_voice_state_update(member, before, after):
    voice = discord.utils.get(bot.voice_clients, guild=member.guild)
    await asyncio.sleep(2)
    if voice and voice.is_connected():
        if len(voice.channel.members) == 1:
            await voice.disconnect()


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def play(ctx, *arg):
    msg = "play"
    for i in arg:
        msg = str(msg) + " " + i
    await DevCommands.write_logs(ctx, msg)
    if arg:
        if ctx.message.author.voice is None:
            await ctx.send("Вы не подключены к голосовому каналу")
        else:
            await ctx.send("Поиск")
            await Play.play(ctx, *arg)
    else:
        await ctx.send("Напишите что вы хотите включить")


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def replay(ctx, *arg):
    msg = "replay"
    for i in arg:
        msg = str(msg) + " " + i
    await DevCommands.write_logs(ctx, msg)
    if arg:
        if ctx.message.author.voice is None:
            await ctx.send("Вы не подключены к голосовому каналу")
        else:
            await ctx.send("Поиск")
            await Replay.replay(ctx, *arg)
    else:
        await ctx.send("Напишите что вы хотите включить")


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def stop(ctx):
    await DevCommands.write_logs(ctx, "stop")
    if ctx.message.author.voice is None:
        await ctx.send("Вы не подключены к голосовому каналу")
    else:
        if ctx.guild.voice_client.channel == ctx.message.author.voice.channel:
            await ctx.send("Видео остановлено")
            await SupportCommands.stop(ctx, bot)
        else:
            await ctx.send('Бот находится в другом канале')


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def stop_replay(ctx):
    await DevCommands.write_logs(ctx, "stop_replay")
    await Replay.stop_replay(ctx, bot)


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def leave(ctx):
    await DevCommands.write_logs(ctx, "leave")
    if ctx.message.author.voice is None:
        await ctx.send("Вы не подключены к голосовому каналу")
    else:
        if ctx.guild.voice_client.channel == ctx.message.author.voice.channel:
            await SupportCommands.leave(ctx, bot)
        else:
            await ctx.send('Бот находится в другом канале')


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def pause(ctx):
    await DevCommands.write_logs(ctx, "pause")
    if ctx.message.author.voice is None:
        await ctx.send("Вы не подключены к голосовому каналу")
    else:
        if ctx.guild.voice_client.channel == ctx.message.author.voice.channel:
            await ctx.send("Видео на паузе")
            await SupportCommands.pause(ctx, bot)
        else:
            await ctx.send('Бот находится в другом канале')


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def resume(ctx):
    await DevCommands.write_logs(ctx, "resume")
    if ctx.message.author.voice is None:
        await ctx.send("Вы не подключены к голосовому каналу")
    else:
        if ctx.guild.voice_client.channel == ctx.message.author.voice.channel:
            await ctx.send("Видео возобновлено")
            await SupportCommands.resume(ctx, bot)
        else:
            await ctx.send('Бот находится в другом канале')


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def logs(ctx, *date):
    msg = "logs"
    for i in date:
        msg = str(msg) + " " + i
    await DevCommands.write_logs(ctx, msg)
    if date:
        await DevCommands.get_logs(ctx, *date)
    else:
        await ctx.send("Введите дату за какую вы хотите получить логи")


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def help(ctx):
    await DevCommands.write_logs(ctx, "help")
    await SupportCommands.help(ctx)


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def get(ctx, url):
    if url:
        msg = "get " + url
        await DevCommands.write_logs(ctx, msg)
        await DevCommands.get(ctx, url)
    else:
        await ctx.send("Введите ссылку на сайт откуда хотите получить код")


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def spam(ctx, *args):
    msg = "spam"
    for i in args:
        msg = str(msg) + " " + i
    await DevCommands.write_logs(ctx, msg)
    await TrollCommands.spam(ctx, *args)


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def switch(ctx):
    await DevCommands.write_logs(ctx, "switch")
    await TrollCommands.switch(ctx)


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def ssearch(ctx, *name):
    msg = "ssearch"
    for i in name:
        msg = str(msg) + " " + i
    await DevCommands.write_logs(ctx, msg)
    await SpotifyPlay.ssearch(ctx, *name)


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def splay(ctx, *name):
    await SpotifyPlay.splay(ctx, *name)


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def chat(ctx, *question):
    if question:
        msg = "ssearch"
        for i in question:
            msg = str(msg) + " " + i
        await DevCommands.write_logs(ctx, msg)
        await ctx.send("Обрабатываю запрос")
        await ChatGPT.chat(ctx, *question)
    else:
        await ctx.send("Напишите, что хотите спросить у бота")


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def game(ctx, *name):
    if name:
        msg = "game"
        for i in name:
            msg = str(msg) + " " + i
        await DevCommands.write_logs(ctx, msg)
        await ctx.send("Ищу игру")
        await SteamCommands.game(ctx, *name)
    else:
        await ctx.send("Напишите название игры")

bot.run(key)

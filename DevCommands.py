import datetime
import json
import os
import datetime
import mimetypes
import tempfile

import discord
import requests

with open('source.json') as file:
    source = json.load(file)
    log = source['logs_path'][0]['log']


def get_current_minute():
    minutes = datetime.datetime.now()
    return "<" + str(minutes.hour) + "h " + str(minutes.minute) + "m " + str(minutes.second) + "s" + ">"


def get_current_time():
    cur_time = datetime.datetime.now()
    return str(cur_time.day) + "-" + str(cur_time.month) + "-" + str(cur_time.year)


async def work_withFile(path, id_user, channel, author, args, mode):
    file = open(path, f'{mode}')
    text = id_user.mention + "(" + author + ")" + " " + "channel" + "(" + str(
        channel) + ")" + " " + args + " " + get_current_minute()
    file.write(text + '\n')
    file.close()


async def write_logs(ctx, args):
    server = ctx.guild.name
    channel = ctx.message.channel
    author = ctx.message.author.name
    id_user = ctx.message.author
    directory = f'{log}\\{server}'
    check_dir = os.path.isdir(directory)
    if check_dir is True:
        path = f'{directory}\\{get_current_time()}.txt'
        check = os.path.isfile(path)
        if check is True:
            await work_withFile(path, id_user, channel, author, args, 'a')
        else:
            await work_withFile(path, id_user, channel, author, args, 'w')
    else:
        os.mkdir(directory)
        path = f'{directory}\\{get_current_time()}.txt'
        check = os.path.isfile(path)
        if check is True:
            await work_withFile(path, id_user, channel, author, args, 'a')
        else:
            await work_withFile(path, id_user, channel, author, args, 'w')


async def get_logs(ctx, *date):
    this_date = ""
    for i in date:
        this_date = str(this_date) + i + " "
    code_date = this_date
    if this_date.index('0') == 0:
        code_date = this_date[:0] + this_date[1:]
    if this_date.index('0') == 3:
        code_date = this_date[:3] + this_date[4:]
    if code_date.index('0') == 2:
        code_date = code_date[:2] + code_date[3:]
    if "." in code_date:
        code_date = code_date[:-1]
        new_date = code_date.replace('.', '-')
    if "/" in code_date:
        code_date = code_date[:-1]
        new_date = code_date.replace('/', '-')
    if " " in code_date:
        code_date = code_date[:-1]
        new_date = code_date.replace(' ', '-')
    server = ctx.guild.name
    directory = f'{log}\\{server}'
    check_dir = os.path.isdir(directory)
    if check_dir is True:
        path = f'{directory}\\{new_date}.txt'
        check = os.path.isfile(path)
        if check is True:
            await ctx.send(file=discord.File(path))
        else:
            await ctx.send('За эту дату нет логов')
    else:
        await ctx.send('Нету логов для вашего сервера')


async def get(ctx, url: str):
    REQUEST_TIMEOUT = 10

    # Make request
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)

    except requests.exceptions.Timeout:
        await ctx.send('Превышено время ожидания ответа от сервера')
        return

    except requests.exceptions.RequestException as e:
        await ctx.send(str(e))
        return

    if len(resp.content) > 8 * 1024 * 1024:
        await ctx.send('Файл слишком большой')
        return

    # Get file extension
    content_type = resp.headers.get('Content-Type')

    if content_type is None:
        ext = '.txt'
    else:
        mime = content_type.split(';')[0]
        ext = mimetypes.guess_extension(mime)
        if ext is None:
            ext = '.txt'

    # Send as text if it's text
    if mime.startswith('text/') and len(resp.text) < 2000:
        await ctx.send(resp.text)
        return

    # Send as file
    with tempfile.TemporaryFile() as f:
        f.write(resp.content)
        f.seek(0)

        await ctx.send(file=discord.File(f.file, 'file' + ext))

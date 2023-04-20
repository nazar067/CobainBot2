import asyncio

import discord


async def help(ctx):
    embed = discord.Embed(
        title='YouTube',
        description=f'$play - команда для проигрывания музыки или видео, $play url или название видео/песни\n'
                    "\n"
                    "$replay - команда для зацикливания музыки или видео. $replay url или название видео/песни\n"
                    "чтобы выключить видео используйте $stop_replay\n"
                    "\n"
                    "$leave - команда чтобы выгнать бота с канала. $leave\n"
                    "\n"
                    "$stop - команда чтобы остановить музыку/видео. $stop\nпри replay музыка/видео перезапускается\n"
                    "\n"
                    "$stop_replay - команда чтобы остановить зацикливание музыку/видео. $stop_replay\n"
                    "\n"
                    "$pause - команда чтобы поставить музыку/видео на паузу. $pause\n"
                    "\n"
                    "$resume - команда чтобы продолжить музыку/видео. $resume\n"
                    "\n",
        colour=discord.Color.yellow(),
    )
    embed.add_field(name="Dev commands",
                    value="$spam - команда, чтобы спамить определенный текст. $spam (текст) (количество повторений) ("
                          "задержка в секундах(от 0.5 до 60)) к примеру, $spam hello 100 1\n "
                          "\n"
                          "$switch - остановить команду $spam. $switch\n"
                          "\n"
                          "$get - команда, чтобы просмотреть исходный код html страницы. $get url\n"
                          "\n"
                          "$logs - команда чтобы посмотреть логи вашего сервера. $logs date(место date вводите дату, "
                          "к примеру 01.01.2023)\n",
                    )
    embed.add_field(name="Spotify",
                    value="$ssearch - команда чтобы получить ссылку на песню в Spotify. $ssearch название песни\n"
                    )
    embed.add_field(name="Steam",
                    value="$game - команда чтобы получить информацию об игре в Steam. $game название игры(точно такое "
                          "же как в Steam)\n "
                    )
    await ctx.send(embed=embed)


async def stop(ctx, bot):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    else:
        await ctx.send("Сейчас ничего не проигрывается")


async def leave(ctx, bot):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Бот не подключен ни к одному каналу")


async def pause(ctx, bot):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Сейчас ничего не проигрывается")


async def resume(ctx, bot):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Сейчас ничего нету на паузе")

import asyncio
from asyncio import sleep


is_running = {}


async def spam(ctx, *args):
    global is_running
    server_id = str(ctx.guild.id)
    is_running[server_id] = True

    string = None
    repeats = None
    delay = None

    try:
        string = args[0]
        repeats = int(args[1])
        delay = float(args[2])

    except:
        await ctx.send('Изначально пишешь, что нужно спамить, потом количество, потом задержку в секундах (0.5 - 60)')
        return

    if delay < 0.5 or delay > 60:
        await ctx.send('Задержка должна быть в пределах между 0.5 и 60 секундами.')
        return

    for i in range(repeats):
        if server_id in is_running and not is_running[server_id]:
            break
        else:
            await ctx.send(string)
            await sleep(delay)


async def switch(ctx):
    global is_running
    server_id = str(ctx.guild.id)
    is_running[server_id] = False

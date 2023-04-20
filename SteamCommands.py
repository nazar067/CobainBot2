import json

import discord
import requests
from bs4 import BeautifulSoup

with open('source.json') as file:
    source = json.load(file)
    api_key = source['steam'][0]['API_key']


async def game(ctx, *name):
    response = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0002/')
    games = response.json()['applist']['apps']

    # Находим ID игры по ее имени
    game_name = ''
    for arg in name:
        game_name = str(game_name) + arg + " "
    game_name = game_name[:-1]
    game_id = None
    for game in games:
        if game['name'].lower() == game_name.lower():
            game_id = game['appid']
            break

    if game_id is not None:
        # Получаем информацию об игре по ее ID
        response = requests.get(f'http://store.steampowered.com/api/appdetails?appids={game_id}&cc=ua&l=russian')
        game_info = response.json()[str(game_id)]['data']

        pc_requirements = game_info['pc_requirements']
        minimum_soup = BeautifulSoup(pc_requirements['minimum'], 'html.parser')
        minimum_list = minimum_soup.find_all('li')
        minimum_req = []
        for li in minimum_list:
            minimum_req.append(li.text.strip())
        min_rqmnts = "\n{}".format('\n'.join(minimum_req))

        recommended_soup = BeautifulSoup(pc_requirements['recommended'], 'html.parser')
        recommended_list = recommended_soup.find_all('li')
        recommended_req = []
        for li in recommended_list:
            recommended_req.append(li.text.strip())
        rec_rqmnts = "\n{}".format('\n'.join(recommended_req))

        soup = BeautifulSoup(game_info['detailed_description'], 'html.parser')
        description = soup.get_text()

        url = f"https://store.steampowered.com/app/{game_id}"
        if game_info['is_free']:
            embed = discord.Embed(
                title="Game info",
                description=f"Название игры: {game_info['name']}\n"
                            f"\n"
                            f"Описание игры: {description}\n"
                            f"\n"
                            f"Ссылка на игру: {url}\n"
                            f"\n"
                            f"Цена игры: Бесплатно\n"
                            f"\n"
                            f"Разработчик: {game_info['developers'][0]}\n"
                            f"\n"
                            f"Издатель: {game_info['publishers'][0]}\n"
                            f"\n",
                colour=discord.Colour.green()
            )
            embed.add_field(name="Минимальные cистемные требования",
                            value=f"{min_rqmnts}"
                            )
            embed.add_field(name="Рекомендованые cистемные требования",
                            value=f"{rec_rqmnts}"
                            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Game info",
                description=f"Название игры: {game_info['name']}\n"
                            f"\n"
                            f"Описание игры: {description}\n"
                            f"\n"
                            f"Ссылка на игру: {url}\n"
                            f"\n"
                            f"Цена игры: {game_info['price_overview']['final_formatted']}\n"
                            f"\n"
                            f"Разработчик: {game_info['developers'][0]}\n"
                            f"\n"
                            f"Издатель: {game_info['publishers'][0]}\n"
                            f"\n",
                colour=discord.Colour.green()
            )
            embed.add_field(name="Минимальные cистемные требования",
                            value=f"{min_rqmnts}"
                            )
            embed.add_field(name="Рекомендованые cистемные требования",
                            value=f"{rec_rqmnts}"
                            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='Game info',
            description=f"Игра с названием '{game_name}' не найдена в Steam",
            colour=discord.Color.red(),
        )
        await ctx.send(embed=embed)

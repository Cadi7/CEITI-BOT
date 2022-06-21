# bot.py
import os

import discord

import scrape
from bs4 import BeautifulSoup
import requests
from discord.ext import commands

TOKEN = 'NzIzMDkwMDgwNjAzOTYzNDQz.Xuskew.bovs81LDuz8XdC-rGsQW3qQyOOM'
GUILD = '636288911538389032'
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print(
        f'{client.user} tocmai s-a conectat pe server\n'
    )


@client.command()
async def ping(ctx):
    await ctx.send('Pong!')


async def test(ctx, arg):
    await ctx.send(arg)


@client.command()
async def idnp(ctx, idnp):
    parametru = {'idnp': idnp}
    with requests.session() as s:
        url = "https://api.ceiti.md/date/login"
        cerere = s.post(url, data=parametru)

        pagina = BeautifulSoup(cerere.text, 'html.parser')
        with open("pagina.html", "w", encoding="utf-8") as file:
            file.write(str(pagina))
        table = pagina.find("table", attrs={"class": "table table-bordered table-condensed table-hover table-white"})
    data = []

    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    embedVar = discord.Embed(title="Date personale", description=" ", color=0x00ff00)
    embedVar.add_field(name="Nume", value=str(data[0][0]), inline=True)
    embedVar.add_field(name="Prenume", value=str(data[1][0]), inline=True)
    embedVar.add_field(name="Patronimic", value=str(data[2][0]), inline=True)
    embedVar.add_field(name="Anul de studii", value=str(data[3][0]), inline=True)
    embedVar.add_field(name="Grupa", value=str(data[4][0]), inline=True)
    embedVar.add_field(name="Specialitatea", value=str(data[5][0]), inline=True)
    embedVar.add_field(name="Diriginte", value=str(data[6][0]), inline=True)
    embedVar.add_field(name="Sef de sectie", value=str(data[7][0]), inline=True)
    await ctx.send(embed=embedVar)


client.run(TOKEN)

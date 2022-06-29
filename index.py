import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

TOKEN = ''
client = commands.Bot(command_prefix='!',intents=intents)

butoane = [
        "Date personale",
        "Semestrul 1",
        "Semestrul 2",
        "Examen Sem 1",
        "Examen Sem 2",
        "Examen Sem 3",
        "Examen Sem 4",
        "Examen Sem 5",
        "Examen Sem 6",
        "Examen Sem 7",
        "Examen Sem 8",
    ]

@client.command()
async def idnp(ctx, idnp):
    #await ctx.message.delete()
    tmp_mess = await ctx.send(f"Procesarea informației pentru {ctx.message.author.display_name}")
    parametru = {'idnp': idnp}

    global butoane

    embeds = {}
    with requests.session() as s:
        url = "https://api.ceiti.md/date/login"
        cerere = s.post(url, data=parametru)

        pagina = BeautifulSoup(cerere.text, 'html.parser')
        tables = pagina.find_all("table")

        for i in range(7):
            tables.pop()

        for i, table in enumerate(tables):
            data = []
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all("th") + row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                data.append(cols)

            embedVar = discord.Embed(title=butoane[i], description="", color=0x00ff00)
            for v in data:
                if v[1] != "" and v[1] != "Note" and v[1] != "Nota":
                    embedVar.add_field(name=v[0], value=v[1])
            embeds[butoane[i]] = embedVar

    class Dropdown(discord.ui.Select):
        def __init__(self):
            options = [discord.SelectOption(label=opt) for opt in butoane]

            super().__init__(placeholder='Alege optiunea', min_values=1, max_values=1, options=options)

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.edit_message(embed=embeds[self.values[0]])


    class DropdownView(discord.ui.View):
        def __init__(self):
            super().__init__()

            self.add_item(Dropdown())

    await ctx.send(embed=embeds[butoane[0]],view=DropdownView())


client.run(TOKEN)

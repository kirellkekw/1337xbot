import nextcord
from nextcord.ext import commands
import os

token = os.getenv("DISCORD_TOKEN")

intents = nextcord.Intents.all()

prefix = '.'

bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.load_extension("torrent")

bot.run(token)

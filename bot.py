import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sys

load_dotenv()
PREFIX = os.getenv('PREFIX')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OWM_TOKEN = os.getenv('OWM_TOKEN')

bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX))

@bot.event
async def on_ready():
    print(f' {bot.user} has connected to Discord!'); sys.stdout.flush()

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

bot.run(DISCORD_TOKEN)

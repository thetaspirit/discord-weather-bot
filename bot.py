import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sys
import weather_helper

load_dotenv()
PREFIX = os.getenv('PREFIX')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX))

@bot.event
async def on_ready():
    print(str(bot.user) + " has connected to Discord!"); sys.stdout.flush()
    weather_helper.initialize()

@bot.command()
async def ping(ctx, *args):
    await ctx.send("pong!")

@bot.command()
async def weather(ctx, *args):
    """
    Gets the current weather of a specified location.
    For location parameters, provide either:
    - a city name
    - a city name and state code
    - a city name, state code, and ISO 3166 2-letter alpha country code
    - city ID
    Make sure each parameter is separated by one space.  Not case-sensitive
    """
    await ctx.send(embed=weather_helper.get_current_weather(args))

bot.run(DISCORD_TOKEN)

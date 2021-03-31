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
async def weather(ctx, *, args): # Note args is a string, not a tuple like other command methods.
    """See docs for weather_helper.get_current_weather()."""
    async with ctx.typing(): em = weather_helper.get_current_weather(args)
    await ctx.send(embed=em)
    sys.stdout.flush()

@bot.command()
async def air(ctx, *, args): # Note args is a string, not a tuple like other command methods.
    """See docs for weather_helper.air()."""
    async with ctx.typing(): em = weather_helper.air(args)
    await ctx.send(embed=em)
    sys.stdout.flush()

@bot.command()
async def units(ctx, *args):
    """Either sets the units to the specified type, or returns the current unit setting."""
    async with ctx.typing(): msg = weather_helper.units(args)
    await ctx.send(msg)
    sys.stdout.flush()

bot.run(DISCORD_TOKEN)

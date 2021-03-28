import requests
import json
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Bellevue,wa,us&appid=a66f486e572402ca03418ef1ad2487eb&units=metric")
raw_data = response.json()
print(response.status_code)
print(type(raw_data))
print(raw_data)

#  data = json.loads(response.json())

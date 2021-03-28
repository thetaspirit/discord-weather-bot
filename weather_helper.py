import json
import requests
import os
import sys
import discord
import time_helper

def initialize():
    global OWM_TOKEN
    OWM_TOKEN = os.getenv('OWM_TOKEN')

    global UNITS
    UNITS = "imperial"
    #default to imperial units

    global units_dict
    units_dict = {"imperial": {"temp": "°F", "speed": "mph", "pressure": "hPa"}, 
                  "metric": {"temp": "°C", "speed": "m/s", "pressure": "hPa"}, 
                  "standard": {"temp": "°K", "speed": "m/s", "pressure": "hPa"}}

    global city_codes
    city_codes = json.load(open('city.list.json'))
    """A list of dictionaries.  Each dictionary is info about a city"""

    print("Weather helper initialized!"); sys.stdout.flush()

def find_city_from_id(id):
    """Finds city from city_codes list based on id number.  Returns dictionary object."""
    return [city for city in city_codes if city["id"] == id][0]

def get_current_weather(args):
    """
    Takes in a tuple for location data, one of the following:
    - a city name
    - a city name and state code
    - a city name, state code, and country ISO 3155 2-letter code
    - a city ID
    Returns a Discord Embed object (or a string if there's an error).
    """
    url = ""
    if len(args) == 1 & args[0].isnumeric():
    # finds location by city code from json file
        url = "https://api.openweathermap.org/data/2.5/weather?id=" + str(args[0])
    else:
        q = ""
        for i in range(len(args)):
            q += args[i]
            if i < (len(args) - 1):
                q += ","
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + q

    url += "&units=" + UNITS + "&appid=" + OWM_TOKEN
    
    response = requests.get(url)
    data = response.json()

    # if the response code isn't 200, it automatically exits the function, and returns the error code.
    if response.status_code != 200:
        return "error " + str(response.status_code) + " " + data["message"]

    location = find_city_from_id(data["id"]) #data["id"] is an int
    
    # making the embed
    embed_title = data["weather"][0]["description"].title() + " " + str(data["main"]["temp"]) + units_dict[UNITS]["temp"]
    embed_description = "Weather for **" + location["name"] + ", " + location["state"] + " " + location["country"] + "** at "
    embed_description += time_helper.get_time_with_timezone(data["timezone"])
    embed_colour = 0x32A852

    embed = discord.Embed(title=embed_title, description=embed_description, colour=embed_colour)
    return embed

def get_temp_color(temp):
    """Returns a hex color depending on the temp and temperature units."""

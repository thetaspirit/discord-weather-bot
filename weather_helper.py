import json
import requests
import os
import sys
import discord
import urllib.parse
from unidecode import unidecode
import assets
import time_helper

def initialize():
    global OWM_TOKEN
    OWM_TOKEN = os.getenv('OWM_TOKEN')

    global UNITS
    UNITS = "imperial"
    #default to imperial units

    global units_dict
    units_dict = assets.units_dict

    global city_codes
    city_codes = json.load(open('city.list.json'))
    """A list of dictionaries.  Each dictionary is info about a city"""

    print("Weather helper initialized!"); sys.stdout.flush()

def find_city_from_id(id):
    """Finds city from city_codes list based on id number.  Returns dictionary object."""
    return [city for city in city_codes if city["id"] == id][0]
    # there should only be one item in this dict bc id numbers are unique

def find_city_from_name(args):
    """Takes same inputs as weather method. Separated by spaces and comma-spaces. Returns a dict."""
    location = args.split(",") # might only have commas, not comma-spaces
    name = unidecode(location[0].strip().lower())
    
    # if state is empty
    if len(location) == 3:
        state = unidecode(location[1].strip().lower())
        country = unidecode(location[2].strip().lower())
    # if state or state and country are empty
    else:
        state = ""
        try: country = unidecode(location[1].strip().lower())
        except: country = ""

    cities = [city for city in city_codes if unidecode(city["name"]).lower()) == namne]
    if len(cities) == 1: return cities[0]
    # if country is not blank and we have more than one possible city
    elif country:
        cities = [city for city in cities if unidecode(city["country"]).lower() == country]
        if len(cities) == 1: return cities[0]

    # either the city doesn't have a state, or the user didn't provide it.
    # if there's a place with no state and a place with a state, choose the one with no state.
    cities = [city for city in cities if unidecode(city["state"]).lower() == state]
    
    try: return cities[0]
    except: return {}

def get_current_weather(args):
    """
    Takes in a string for location data, one of the following:
    - <city name>
    - <city name>, <ISO 3166 country code, 2 letters>
    - <city name>, <state code, 2 letters>, <ISO 3166 country code>
    - a city ID number
    Use a space if the city name has more than one word (like normal).
    Separate 
    Returns a Discord Embed object
    """
    global UNITS
    global units_dict
    global OWM_TOKEN
    global city_codes

    url = ""
    if args.isnumeric():
    # uses city code instead of city/location name
        url = "https://api.openweathermap.org/data/2.5/weather?id=" + str(args)
    else:
        args = parse_location_url(args)
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + args

    url += "&units=" + UNITS + "&appid=" + OWM_TOKEN
    
    print(url)
    response = requests.get(url)
    data = response.json()

    # if the response code isn't 200, it automatically exits the function, and returns the error code.
    if response.status_code != 200:
        return discord.Embed(title="error " + str(response.status_code) + ": " + data["message"])

    location = find_city_from_id(data["id"]) #data["id"] is an int
    
    # making the embed
    embed_title = data["weather"][0]["description"].title() + " " + str(data["main"]["temp"]) + units_dict[UNITS]["temp"]
    embed_description = "Weather for **" + location["name"] + ", " + location["state"] + " " + location["country"] + "** at "
    embed_description += time_helper.get_time_with_timezone(data["timezone"])
    embed_colour = get_temp_color()
    image_url = "http://openweathermap.org/img/wn/" + str(data["weather"][0]["icon"]) + "@2x.png"

    embed = discord.Embed(title=embed_title, description=embed_description, colour=embed_colour)
    embed.set_thumbnail(url=image_url)

    temperature_value = "It's " + str(data["main"]["temp"]) + units_dict[UNITS]["temp"]
    temperature_value += ".  Feels like " + str(data["main"]["feels_like"]) + units_dict[UNITS]["temp"]
    embed.add_field(name="Temperature", value=temperature_value, inline=False)

    embed.add_field(name="Pressure", value=str(data["main"]["pressure"]) + " hPa")
    embed.add_field(name="Humidity", value=str(data["main"]["humidity"]) + "%")
    embed.add_field(name="Visibility", value=str(data["visibility"]) + " meters")

    try:
        wind_value = "Speed: " + str(data["wind"]["speed"]) + " " + units_dict[UNITS]["speed"]
        wind_value += ".  Direction: " + str(data["wind"]["deg"]) + "°"
        embed.add_field(name="Wind", value=wind_value)
    except: pass

    try: embed.add_field(name="Cloud cover", value=str(data["clouds"]["all"]) + "%")
    except: pass

    try:
        rain_value = str(data["rain"]["1h"]) + " mm of rain in the past hour.  "
        try: rain_value += str(data["rain"]["3h"]) + " mm of rain in the past three hours."
        except: pass
        embed.add_field(name="Rain", value=rain_value, inline=False)
    except: pass

    try:
        snow_value = str(data["snow"]["1h"]) + " mm of snow in the past hour.  "
        try: snow_value += str(data["snow"]["3h"]) + " mm of snow in the past three hours."
        except: pass
        embed.add_field(name="Snow", value=snow_value, inline=False)
    except: pass
    
    return embed

def air(args):
    """Stats about air quality. Takes in location and translates to lat and log."""
    global UNITS
    global units_dict
    global OWM_TOKEN
    global city_codes

def units(args):
    global UNITS
    if args and args[0] in units_dict.keys():
        UNITS = args[0]
        return "Units successfully set to " + UNITS
    else:
        return "Units not changed.  Current units are " + UNITS + ".  Options for units are \"standard\", \"metric\", or \"imperial\"."

def parse_location_url(args):
    """Takes in a string with spaces and commas and spaces.  ex: New York City, NY, US"""
    args = args.replace(", ", ",")
    args = urllib.parse.quote(args)
    return args

def get_temp_color():
    """Returns a hex color depending on the temp and temperature units."""
    return 0x32A852

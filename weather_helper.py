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

def find_city_from_id(number):
    """Finds city from city_codes list based on id number.  Returns dictionary object."""
    # there should only be one item in this dict bc id numbers are unique
    return [city for city in city_codes if city["id"] == number][0]

def find_city_from_name(args):
    """Takes same inputs as weather method. **Assumes second parameter is country if there are only 2 parameters.**
    Separated by spaces and comma-spaces. Returns a array of dicts.Use first dict. If returns empty, can't find city.
    MUST HAVE A COUNTRY"""
    
    location = args.split(",") # might only have commas, not comma-spaces
    try: name = unidecode(location[0].strip().lower())
    except: return {}
    
    ### PARSING INPUT: finding city name, state, and country
    # if state is empty
    if len(location) == 3:
        state = unidecode(location[1].strip().lower())
        country = unidecode(location[2].strip().lower())
    # if state or state and country are empty
    else:
        # if there are only 2 params, assumes it's the country, not the state
        try: country = unidecode(location[1].strip().lower()); state = ""
        except: return {} # must provide a country

    ### SEARCHING FOR CITY
    cities = [city for city in city_codes if unidecode(city["name"]).lower() == name]
    if len(cities) < 2: return cities

    cities = [city for city in cities if unidecode(city["country"]).lower() == country]
    if len(cities) < 2: return cities

    if state: cities = [city for city in cities if unidecode(city["state"]).lower() == state];
    
    # if state is empty, but there are matches for cities without states, use those
    elif [city for city in cities if unidecode(city["state"]).lower() == state]: 
        cities = [city for city in cities if unidecode(city["state"]).lower() == state]

    return cities

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
    
    response = requests.get(url)
    data = response.json()

    # if the response code isn't 200, it automatically exits the function, and returns the error code.
    if response.status_code != 200:
        return discord.Embed(title="error " + str(response.status_code), description=data["message"])

    city = find_city_from_id(data["id"]) #data["id"] is an int
    
    # making the embed
    embed_title = data["weather"][0]["description"].title() + " " + str(data["main"]["temp"]) + units_dict[UNITS]["temp"]
    embed_description = "Weather for **" + city["name"] + ", " + city["state"] + " " + city["country"] + "** at "
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

    uv_index = requests.get("https://api.openweathermap.org/data/2.5/uvi?lat=" + str(data["coord"]["lat"]) + "&lon=" + str(data["coord"]["lon"]) + "&appid=" + OWM_TOKEN).json()["value"]
    embed.add_field(name="UV Index", value=str(uv_index))

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
    """Stats about air quality. Takes in location and translates to lat and lon."""
    global UNITS
    global units_dict
    global OWM_TOKEN

    try: city = find_city_from_name(args)[0] # otherwise, city could not be found
    except: return discord.Embed(title="Cannot find city", description="Please provide `<city>, <country>` or `<city>, <state>, <country>`")

    url = "https://api.openweathermap.org/data/2.5/air_pollution?lat=" + str(city["coord"]["lat"]) + "&lon=" + str(city["coord"]["lon"]) + "&appid=" + OWM_TOKEN
    response = requests.get(url)
    
    if response.status_code != 200:
        return discord.Embed(title="error " + str(respons(e.status_code), description=data["message"]))

    data = response.json()

    air_quality_index = data["list"][0]["main"]["aqi"]

    embed_title = "Air Quality Index: " + str(air_quality_index) + " (on a scale of 1-5)"
    embed_description = "Air pollution data for **" + city["name"] + ", " + city["state"] + " " + city["country"] + "**"
    
    embed_colour = 0xFFFFFF
    if air_quality_index == 1: embed_colour = 0xFF0000
    elif air_quality_index == 2: embed_colour = 0xFF7F00
    elif air_quality_index == 3: embed_colour = 0xFFFF00
    elif air_quality_index == 4: embed_colour = 0x7FFF00
    elif air_quality_index == 5: embed_colour = 0x00FF00

    embed = discord.Embed(title=embed_title, description=embed_description, colour=embed_colour)

    embed.add_field(name="Carbon Monoxide", value=str(data["list"][0]["components"]["co"]) + " μg/m³")
    embed.add_field(name="Nitrogen Monoxide", value=str(data["list"][0]["components"]["no"]) + " μg/m³")
    embed.add_field(name="Nirogen Dioxide", value=str(data["list"][0]["components"]["no2"]) + " μg/m³")
    embed.add_field(name="Ozone", value=str(data["list"][0]["components"]["o3"]) + " μg/m³")
    embed.add_field(name="Sulphur Dioxide", value=str(data["list"][0]["components"]["so2"]) + " μg/m³")
    embed.add_field(name="Fine Particulate Matter", value=str(data["list"][0]["components"]["pm2_5"]) + " μg/m³")
    embed.add_field(name="Coarse Particulate Matter", value=str(data["list"][0]["components"]["pm10"]) + " μg/m³")
    embed.add_field(name="Ammonia", value=str(data["list"][0]["components"]["nh3"]) + " μg/m³")

    return embed

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

### THE GEOCODING API DOESN'T PROVIDE ALL THE INFORMATION I NEED.  USING MY OWN GET_CITY_FROM_NAME FUNCTION INSTEAD
#  def find_coords_from_name(args):
    #  """Gets the [lat, lon] coordinates of a city based on its name. Returns empty array if city not found"""
    #  global OWM_TOKEN
    #  args = parse_location_url(args)
    #  url = "https://api.openweathermap.org/geo/1.0/direct?q=" + args + "&limit=1&appid=" + OWM_TOKEN
    #  response = requests.get(url)
    #  if response.status_code != 200: return []
    #  data = response.json()
    #  return [data["lat"], data["lon"]]

def get_temp_color():
    """Returns a hex color depending on the temp and temperature units."""
    return 0x32A852

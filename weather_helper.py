import json
import requests
import os
import sys


def initialize():
    global OWM_TOKEN
    OWM_TOKEN = os.getenv('OWM_TOKEN')

    #  global city_codes = json.load(open('city.list.json'))
    """A list of dictionaries.  Each dictionary is info about a city"""

    print("weather helper initialized!"); sys.stdout.flush()

def find_city_from_id(id):
    """Finds city from city_codes list based on id number.  Returns dictionary object."""
    return [city for city in city_codes if city["id"] == id]

def get_current_weather(args):
    """
    Takes in a tuple for location data, one of the following:
    - a city name
    - a city name and state code
    - a city name, state code, and country ISO 3155 2-letter code
    - a city ID
    """
    if len(args) == 1 & args[0].isnumeric():
    # finds location by city code from json file
        print(type(OWM_TOKEN))
        url = "https://api.openweathermap.org/data/2.5/weather?id=" + str(args[0]) + "&appid=" + OWM_TOKEN
        response = requests.get(url)
        print(response.json())
        print(response.status_code)
        sys.stdout.flush()

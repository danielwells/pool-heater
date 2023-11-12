from os import getenv
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from datetime import datetime

class Utils:
    def __init__(self):
        self.OWM = OWM(getenv('OPENWEATHER_API_KEY'))
        self.ownMGR = self.OWM.weather_manager()
        #change these coordinates to match your location
        self.lat = 33.230581
        self.lon = -111.554867



    def get_weather(self):
        observation = self.ownMGR.weather_at_coords(self.lat, self.lon)
        weather = observation.weather
        return weather

# test = Utils()

# weather = test.get_weather()

# print(datetime.fromtimestamp(weather.srise_time))
# print(datetime.fromtimestamp(weather.sset_time))
# print(weather.temperature('fahrenheit')['temp'])




    

from time import sleep
from os import getenv
import requests
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError

# Change these to match your device
DEVICE_MAC="D03F270C78FE"
DEVICE_MODEL="WLPP1CFH"

class Power:
    def __init__(self):
        self.client = Client()
    
    def login(self):
        response = self.client.login(email=getenv('WYZE_EMAIL'), password=getenv('WYZE_PASSWORD'), key_id=getenv("WYZE_ID"), api_key=getenv("WYZE_KEY"))

    def refresh_login(self):
        response = self.client.refresh_token()
    
    def cycle_power(self, time):
        try:
            plug = self.client.plugs.info(device_mac=DEVICE_MAC)
            print(f"**** Cycling: {plug.nickname} ****")
            response = self.client.plugs.turn_on(device_mac=DEVICE_MAC,  device_model=DEVICE_MODEL)

        except WyzeApiError as e:
            # You will get a WyzeApiError if the request failed
            print(f"Could not start pump: {e}")
            return False
        
        sleep(time)

        try:
            response = self.client.plugs.turn_off(device_mac=DEVICE_MAC,  device_model=DEVICE_MODEL)
            # print(response)

        except WyzeApiError as e:
            # You will get a WyzeApiError if the request failed
            print(f"Could not stop pump: {e}")
            return False
        
        return True
        
# plug = Power()
# plug.login()
# plug.refresh()
# plug.cycle_power(55)
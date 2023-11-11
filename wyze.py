from time import sleep
from os import getenv
import requests
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError

DEVICE_MAC="D03F270C78FE"

class Power:
    def __init__(self):
        self.client = Client()
    
    def login(self):
        response = self.client.login(email=getenv('WYZE_EMAIL'), password=getenv('WYZE_PASSWORD'), key_id=getenv("WYZE_ID"), api_key=getenv("WYZE_KEY"))

    def refresh_login(self):
        response = self.client.refresh_token()
    
    def cycle_power(self, time):
        success=False
        try:
            plug = self.client.plugs.info(device_mac=DEVICE_MAC)
            print(f"**** Cycling: {plug.nickname} ****\n")
            response = self.client.plugs.turn_on(device_mac=DEVICE_MAC,  device_model="WLPP1CFH")

        except WyzeApiError as e:
            # You will get a WyzeApiError if the request failed
            print(f"Could not start pump: {e}")
            return False
        
        sleep(time)

        try:
            response = self.client.plugs.turn_off(device_mac=DEVICE_MAC,  device_model="WLPP1CFH")
            # print(response)

        except WyzeApiError as e:
            # You will get a WyzeApiError if the request failed
            print(f"Could not stop pump: {e}")
            return False
        
        

    def get_status(self):
        session = requests.Session()
        session.auth = (self.username, self.password)
        response = session.get('http://' + self.host + '/wattbox_info.xml')
        print(response.text)
        session.close()

# watt = Power(username=getenv("WATT_USER"), password=getenv("WATT_PASS"), host=getenv("WATT_IP"))
# print(watt.cycle_power(2,10))

# print(getenv('WYZE_PASSWORD'))
# response = Client().login(email=getenv('WYZE_EMAIL'), password=getenv('WYZE_PASSWORD'), key_id=getenv("WYZE_ID"), api_key=getenv("WYZE_KEY"))
# print(f"access token: {response['access_token']}")
# print(f"refresh token: {response['refresh_token']}")
# client = Client(token=response['access_token'])
# print(client.user_get_profile())

'''
try:
    plugs = client.plugs.list()
    plug = client.plugs.info(device_mac=DEVICE_MAC)
    print(plug.nickname)
    response = client.plugs.turn_on(device_mac=DEVICE_MAC,  device_model="WLPP1CFH")
    print(response)
    sleep(3)
    response = client.plugs.turn_off(device_mac=DEVICE_MAC,  device_model="WLPP1CFH")
    print(response)

except WyzeApiError as e:
    # You will get a WyzeApiError if the request failed
    print(f"Got an error: {e}")
'''
# plug = Power()
# plug.login()
# plug.refresh()
# plug.cycle_power(55)
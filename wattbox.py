from time import sleep
from os import getenv
import requests

class Power:
    def __init__(self, username, password, host):
        self.username = username
        self.password = password
        self.host = host
    
    def cycle_power(self, outlet_num, time):
        success=False
        session = requests.Session()
        session.auth = (self.username, self.password)
        response = session.get('http://' + self.host + f'/control.cgi?outlet={outlet_num}&command=1')
        if "outlet_status" in response.text:
            success_on=True
            print("Power On")
        sleep(time)
        response = session.get('http://' + self.host + f'/control.cgi?outlet={outlet_num}&command=0')
        if "outlet_status" in response.text:
            success_off=True
            print("Power Off")
        session.close()
        if success_on and success_off:
            return True
        else:
            return False

    def get_status(self):
        session = requests.Session()
        session.auth = (self.username, self.password)
        response = session.get('http://' + self.host + '/wattbox_info.xml')
        print(response.text)
        session.close()

watt = Power(username=getenv("WATT_USER"), password=getenv("WATT_PASS"), host=getenv("WATT_IP"))
print(watt.cycle_power(2,10))
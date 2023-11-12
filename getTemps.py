import os
import glob
import time
from wyze import Power
from utils import Utils
from datetime import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

SENSOR_POOL = "28-3c2b045727ce"
SENSOR_SOLAR = "28-3c02e3814d3b"
SENSOR_AMBIENT = "28-3c02e3815b4f"
SENSOR_4 = "28-3c560457b7af"
# Avg window in minutes
AVG_WINDOW = 6
TEMP_WAIT = 30
PUMP_RUNTIME = 60

base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')
sensors = {}
solar_temps = []
single_temp_diffs = []
avg_single_temp_diffs = []
avg_single_temp_diff = 0


def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_folder):
    device_file = device_folder + '/w1_slave'
    lines = read_temp_raw(device_file)
    sensor = device_folder.split("/")
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return sensor[-1], temp_f

def average(temps):
    total = 0
    i = 0
    while i < len(temps):
        total = total + temps[i]
        i = i + 1

    avg = total / len(temps)

    return round(avg, 3)

plug = Power()
plug.login()
owm = Utils()
weather = owm.get_weather()
sunrise = datetime.fromtimestamp(weather.srise_time)
sunset = datetime.fromtimestamp(weather.sset_time)

# plug.refresh()
pump_ran = False

# current_hour = datetime.now().strftime("%H")
# if int(current_hour) > 7 and int(current_hour) < 18:
    # isDay = True
# else:
    # isDay = False  

current_hour = datetime.now()
if current_hour > sunrise and current_hour < sunset:
    isDay = True
    print("Is Day")
else:
    isDay = False
    print("Is Not Day")

if isDay:
    isWarming = True
    isCooling = False
else:
    isWarming = False
    isCooling = True


# Initilize avg array to 0
avg_single_temp_diffs.append(0)
single_temp_diffs.append(0)
count = round(AVG_WINDOW*60/TEMP_WAIT) + 1
print(count)

while True:
    for folder in device_folders:
        temp = read_temp(folder)
        sensors[temp[0]] = temp[1]
    # print(sensors)
    solar_temps.append(round(sensors[SENSOR_SOLAR],3))
    if len(solar_temps) > count:
        solar_temps.pop(0)
        single_temp_diffs.pop(0)
        # avg_single_temp_diffs.pop(0)
    if len(solar_temps) >= 2:
        single_temp_diffs.append(round(solar_temps[-1]-solar_temps[-2],3))
        # avg_single_temp_diffs.append(average(single_temp_diffs))
        avg_single_temp_diff = average(single_temp_diffs)

    print(f"{datetime.now().strftime('%m-%d %H:%M:%S')}\tAmbient: {str(round(sensors[SENSOR_AMBIENT],1))}\tBox: {str(round(sensors[SENSOR_SOLAR],1))}\t{AVG_WINDOW}-min Avg Diff: {avg_single_temp_diff}\tLast Diff: {single_temp_diffs[-1]}")
    
    if sensors[SENSOR_SOLAR] > 94 and not pump_ran:
        plug.refresh_login()
        plug.cycle_power(PUMP_RUNTIME)
        pump_ran = True
    else:
        time.sleep(TEMP_WAIT)
        pump_ran = False


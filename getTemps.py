import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

SENSOR_1 = "28-3c2b045727ce"
SENSOR_2 = "28-3c02e3814d3b"

base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')
sensors = {}

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

while True:
    for folder in device_folders:
        temp = read_temp(folder)
        sensors[temp[0]] = temp[1]
    print(sensors)
    print("______________________\n")
    time.sleep(2)


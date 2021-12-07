#!/usr/bin/python
from datetime import datetime
from glob import glob
import json
import os
import time

HOME = os.environ.get('HOME')
TEMPERATURE_FILE = os.path.join(HOME,"RaspTemp/temperature.log")
max_saved_temps = 1000
base_dir = '/sys/bus/w1/devices/'
device_folder = glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(1)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = round((float(temp_string) / 1000.0),1)
        return temp_c

def write_temp_to_file(json_list):
    with open(TEMPERATURE_FILE, 'w') as outfile:
        json.dump(json_list, outfile)

def create_temp_json_object(currenttemperature):
    return ({
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'temperature': currenttemperature
    })

currenttemperature = read_temp()

if not os.path.exists(TEMPERATURE_FILE):
    json_list = {}
    json_list['temperatures'] = []
    json_list['temperatures'].append(create_temp_json_object(currenttemperature))
    write_temp_to_file(json_list)
else:
    with open(TEMPERATURE_FILE) as json_file:
        json_list = json.load(json_file)
        json_sorted = sorted(json_list['temperatures'], key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
        if json_sorted[0]['temperature'] != currenttemperature:
            json_list = {}
            json_list['temperatures'] = json_sorted[0:(max_saved_temps-1)]
            json_list['temperatures'].reverse()
            json_list['temperatures'].append(create_temp_json_object(currenttemperature))
            write_temp_to_file(json_list)
        

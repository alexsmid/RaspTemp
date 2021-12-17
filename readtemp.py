#!/usr/bin/python
from datetime import datetime,timedelta
from glob import glob
import json
import os
import time

HOME = os.environ.get('HOME')
TEMPERATURE_FILE = os.path.join(HOME,"RaspTemp/temperature.log")
number_of_days_displayed = 2
datetoday = datetime.today()
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
        temp_history_list = []
        json_new_list = {}
        json_new_list['temperatures'] = []
        json_new_list['history'] = []
        history_list_grouped_date_list = {} 
        temp_history_date_set = set()
        if len(json_sorted) > 0:
            for line in json_sorted:
                if (datetoday - timedelta(days=number_of_days_displayed)).date() > datetime.strptime(line['date'], '%Y-%m-%d %H:%M:%S').date():
                    temp_history_list.append({'date': line['date'],'temperature': line['temperature']})
                else:
                    json_new_list['temperatures'].append(line)
                    json_new_list['temperatures'].reverse()
                    if json_sorted[0]['temperature'] != currenttemperature:
                        json_new_list['temperatures'].append(create_temp_json_object(currenttemperature))
        for temp_history in temp_history_list:
            temp_history_date_set.add(datetime.strptime(temp_history['date'], '%Y-%m-%d %H:%M:%S').date())
        for temp_history_date in temp_history_date_set:
            temp_history_date_date = temp_history_date.strftime('%Y-%m-%d')
            history_list_grouped_date_list[temp_history_date_date] = []
            for history_list in temp_history_list:
                if (datetime.strptime(history_list['date'], '%Y-%m-%d %H:%M:%S').date().strftime('%Y-%m-%d') == temp_history_date_date):
                    history_list_grouped_date_list[temp_history_date_date].append(history_list)
        for history_list_grouped_date in history_list_grouped_date_list:
            json_new_list['history'].append({
                'date': history_list_grouped_date,
                'min' : min(temp['temperature'] for temp in history_list_grouped_date_list[history_list_grouped_date]),
                'max' : max(temp['temperature'] for temp in history_list_grouped_date_list[history_list_grouped_date]),
                'mean' : round(sum(temp['temperature'] for temp in history_list_grouped_date_list[history_list_grouped_date]) / len(history_list_grouped_date_list[history_list_grouped_date]),1)
            })
        write_temp_to_file(json_new_list)
            

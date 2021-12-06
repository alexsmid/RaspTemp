#!/usr/bin/python
from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from glob import glob
from time import time
from datetime import datetime

app = Flask(__name__)

bootstrap = Bootstrap(app)

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
        temp_c = float(temp_string) / 1000.0
        return temp_c

@app.route("/")
def main():
    while True:
        templateData = {
            'temperature' : read_temp(),
            'updated' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        time.sleep(10)
        return render_template('main.html', **templateData)

if __name__ == "__main__":
    from waitress import serve
    from livereload import Server
    server = Server(app.wsgi_app)
    server.serve(host='0.0.0.0', port=80)

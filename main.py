#!/usr/bin/python
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask import Flask, render_template
import json
import os
import time

app = Flask(__name__)

bootstrap = Bootstrap(app)

TEMPERATURE_FILE = "%TEMPERATUREFILELOCATION%"

@app.route("/")
def main():
    with open(TEMPERATURE_FILE) as json_file:
        json_list = json.load(json_file)
        json_temperatures_sorted = sorted(json_list['temperatures'], key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
        json_temperatures_history_sorted = sorted(json_list['history'], key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    while True:
        templateData = {
            'temperature' : json_temperatures_sorted[0]['temperature'],
            'updated' : json_temperatures_sorted[0]['date'],
            'history' : json_temperatures_sorted[1:],
            'old_history' : json_temperatures_history_sorted
        }
        return render_template('main.html', **templateData)

if __name__ == "__main__":
    from waitress import serve
    #serve(app,host='0.0.0.0', port=80)
    from livereload import Server
    server = Server(app.wsgi_app)
    server.watch(TEMPERATURE_FILE,delay=10)
    server.serve(host='0.0.0.0', port=80)

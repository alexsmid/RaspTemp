#!/usr/bin/python
from flask_bootstrap import Bootstrap
from flask import Flask, render_template
import os
import json
import time


app = Flask(__name__)

bootstrap = Bootstrap(app)

HOME = os.environ.get('HOME')
TEMPERATURE_FILE = os.path.join(HOME,"RaspTemp/temperature.log")

with open(TEMPERATURE_FILE) as json_file:
        json_list = json.load(json_file)
        json_sorted = sorted(json_list['temperatures'], key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'), reverse=True)

@app.route("/")
def main():
    while True:
        templateData = {
            'temperature' : json_sorted[0]['temperature'],
            'updated' : json_sorted[0]['date']
        }
        time.sleep(10)
        return render_template('main.html', **templateData)

if __name__ == "__main__":
    from waitress import serve
    #serve(app,host='0.0.0.0', port=80)
    from livereload import Server
    server = Server(app.wsgi_app)
    server.watch(TEMPERATURE_FILE,delay=10)
    server.serve(host='0.0.0.0', port=80)

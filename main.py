#!/usr/bin/python
from flask_bootstrap import Bootstrap
from flask import Flask, render_template

app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.route("/")
def main():
    templateData = {
        'temperature' : 10,
        'updated' : '2020-01-10'
    }
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    from waitress import serve
    serve(app,host='0.0.0.0', port=80)

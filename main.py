#!/usr/bin/python
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
   templateData = {
      'temperature' : 23,
   }
   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

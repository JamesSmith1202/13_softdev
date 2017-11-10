from flask import Flask, render_template
import urllib2
import json

app = Flask(__name__)
u = urllib2.urlopen("https://api.nasa.gov/planetary/apod?api_key=zCxGtydkrKyrF79TtWItVGYh9KLjhYqBAQzFAbXC")
msg = u.read()
nasa_dict = json.loads(msg)

@app.route("/")
def root():
    return render_template('main.html', img=nasa_dict["url"], information=nasa_dict["explanation"])

if __name__ == "__main__":
    app.run()
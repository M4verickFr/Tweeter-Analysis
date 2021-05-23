# Externe import
import json
from flask import Flask, render_template, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

# Interne import
from database import database

# Setup mysql.connector to authenticate to database
bdd = database("localhost","root","","twitter")
bdd.connect()

#Setup flask server
app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1 per second"],
)
CORS(app)

@app.route('/')
def home():
    """Home page
    """
    return render_template("home.html", tweetNumber=bdd.count("tweet"))

@app.route('/maps/')
def maps():
    """Maps with all tweets in their original position
    """
    tweets = json.dumps(bdd.get_all("tweet"))
    return render_template("maps.html", tweets=tweets)

@app.route('/maps_city/')
def maps_city():
    """Maps with all tweets group by city
    """
    data = {}
    cities = bdd.get_all("city")
    
    for city in cities:
        data[city[0]] = {
            "place_id": city[0],
            "display_name": city[1],
            "polygon": city[2],
            "lat": city[3],
            "lon": city[4],
            "tweets": bdd.request_fetchall(f"SELECT id_tweet FROM tweet WHERE id_city='{city[0]}'")
        }
    
    return render_template("maps_city.html", data=json.dumps(data))

@app.route('/maps_words/')
def maps_words():
    """Cartes avec les 10 mots clés présent dans les tweets par ville
    """
    data = {}
    cities =  bdd.get_all("city")
    
    for city in cities:
        data[city[0]] = {
            "place_id": city[0],
            "display_name": city[1],
            "polygon": city[2],
            "lat": city[3],
            "lon": city[4],
            "tweets": bdd.request_fetchall(f"SELECT id_tweet FROM tweet WHERE id_city='{city[0]}'"),
            "words": bdd.request_fetchall(f"SELECT word, count(*) as 'count'  FROM `word` WHERE id_city='{city[0]}' GROUP BY word ORDER BY count DESC LIMIT 10")
        }
    
    return render_template("maps_words.html", data=json.dumps(data))

if __name__=="__main__":
    app.run(debug=True)
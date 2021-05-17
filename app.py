import json
import tweepy
from flask import Flask, render_template, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

import streaming
from database import database
from keys import *

# Setup tweepy to authenticate with Twitter credentials:
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

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
    tweetNumber = bdd.request_fetchone("SELECT COUNT(*) FROM tweet")
    return render_template("home.html", tweetNumber=tweetNumber)

@app.route('/delete_all_tweets')
def delete_all_tweets():
    bdd.request("DELETE FROM tweet")
    print("Deleting all tweets...")
    return redirect(url_for('home'))

@app.route('/maps/')
def maps():
    tweets = json.dumps(bdd.request_fetchall("SELECT id_tweet, latitude, longitude, full_text FROM tweet"))
    return render_template("maps.html", tweets=tweets)

@app.route('/maps_city/')
def maps_city():
    data = {}
    cities = bdd.request_fetchall("SELECT place_id, lat, lon, display_name, polygon FROM city")
    
    for city in cities:
        data[city[0]] = {
            "place_id": city[0],
            "display_name": city[3],
            "lat": city[1],
            "lon": city[2],
            "polygon": city[4],
            "tweets": bdd.request_fetchall(f"SELECT id_tweet FROM tweet WHERE id_city='{city[0]}'")
        }
    
    return render_template("maps_city.html", data=json.dumps(data))

@app.route('/maps_words/')
def maps_words():
    data = {}
    cities = bdd.request_fetchall("SELECT place_id, lat, lon, display_name, polygon FROM city")
    
    for city in cities:
        data[city[0]] = {
            "place_id": city[0],
            "display_name": city[3],
            "lat": city[1],
            "lon": city[2],
            "polygon": city[4],
            "tweets": bdd.request_fetchall(f"SELECT id_tweet FROM tweet WHERE id_city='{city[0]}'"),
            "words": bdd.request_fetchall(f"SELECT word, count(*) as 'count'  FROM `word` WHERE id_city='{city[0]}' GROUP BY word ORDER BY count DESC LIMIT 10")
        }
    
    return render_template("maps_words.html", data=json.dumps(data))

if __name__=="__main__":
    app.run(debug=True)
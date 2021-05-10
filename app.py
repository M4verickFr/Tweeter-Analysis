import json
import tweepy
import mysql.connector
from flask import Flask, render_template, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

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
    coordinatesNumber = bdd.request_fetchone("SELECT COUNT(*) FROM tweet WHERE latitude != ''")
    
    return render_template("home.html", tweetNumber=tweetNumber, coordinatesNumber=coordinatesNumber)


@app.route('/loading_tweets')
def loading_tweets():
    key_words = ["ia", "adwords", "RGPD", "CNIL", "Cookie"]
    geocodes = ["45.899247,6.129384,50km", "48.856614,2.352222,50km", "45.764043,4.835659,50km"]

    for key_word in key_words:
        for geocode in geocodes:  
            fetched_tweets = api.search(q=key_word,count=100, tweet_mode="extended", lang="fr", geocode=geocode)
            
            print(key_word + " - " + str(len(fetched_tweets)))
            
            for tweet in fetched_tweets:
                try:
                    if tweet.geo == None:
                        sql = "INSERT INTO `tweet`(`id_tweet`, `created_at`, `full_text`, `lang`, `retweet_count`) VALUES (%s,%s,%s,%s,%s)"
                        bdd.insert(sql, (tweet.id_str, tweet.created_at, tweet.full_text, tweet.lang, tweet.retweet_count))
                    else:
                        sql = "INSERT INTO `tweet`(`id_tweet`, `created_at`, `full_text`, `lang`, `retweet_count`, `latitude`, `longitude`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        bdd.insert(sql, (tweet.id_str, tweet.created_at, tweet.full_text, tweet.lang, tweet.retweet_count, tweet.geo["coordinates"][0], tweet.geo["coordinates"][1]))
                except:
                    print("error")
                    print(tweet._json)

    print("Loading tweets...")
    return redirect(url_for('home'))

@app.route('/delete_all_tweets')
def delete_all_tweets():
    bdd.request("DELETE FROM tweet")
    print("Deleting all tweets...")
    return redirect(url_for('home'))

@app.route('/maps/')
def maps():
    tweet_with_coordinates = bdd.request_fetchall("SELECT id_tweet, latitude, longitude FROM tweet WHERE latitude != ''")
    return render_template("maps.html", tweet_with_coordinates=json.dumps(tweet_with_coordinates))

@app.route('/maps_center/')
def maps_center():
    tweet_with_coordinates = bdd.request_fetchall("SELECT id_tweet, latitude, longitude FROM tweet WHERE latitude != ''")
    return render_template("maps_center.html", tweet_with_coordinates=json.dumps(tweet_with_coordinates))

@app.route('/streaming_tweets/')
@limiter.exempt
def streaming_tweets():
    return "@TODO"

@app.route('/maps_streaming/')
def maps_streaming():
    return render_template("maps_streaming.html")

if __name__=="__main__":
    app.run(debug=True)
import json
from geopy.geocoders import Nominatim, Photon
from tweepy import OAuthHandler, Stream, StreamListener, API

import enchant
from nltk import RegexpTokenizer
from nltk.corpus import stopwords

from database import database
from keys import *

class StdOutListener(StreamListener):
    def on_data(self, raw_data):
        self.process_data(raw_data)

    def process_data(self, raw_data):
        try: 
            tweet = json.loads(raw_data)

            if tweet['geo'] is not None:
                places = api.reverse_geocode(tweet["geo"]["coordinates"][0],tweet["geo"]["coordinates"][1], max_result=1, granularity="city")
                
                if (len(places) == 0):
                    print("error: locations not find")
                    return
                
                place = places[0]

                if bdd.request_fetchone(f"SELECT COUNT(*) FROM city WHERE place_id='{place.id}'") == 0:
                    bdd.insert(sql_insert_city, (
                        place.id,
                        place.full_name, 
                        str(place.bounding_box.coordinates),
                        place.centroid[1],
                        place.centroid[0]
                    ))
                    print("city inserted")
                
                if ("extended_tweet" in tweet):
                    text = tweet["extended_tweet"]["full_text"]
                else:
                    text = tweet["text"]
                
                bdd.insert(sql_insert_tweet, (
                    tweet["id_str"],
                    tweet["created_at"], 
                    text, 
                    tweet["lang"], 
                    tweet["retweet_count"],
                    tweet["geo"]["coordinates"][0],
                    tweet["geo"]["coordinates"][1],
                    place.id
                ))
                print("tweet inserted")
                
                words = toknizer.tokenize(text)
                words = list(filter(lambda word: len(word) > 2 and "@" not in word and word[:5] != "https" and word not in stopwords.words('french') and dictonnary.check(word), words))
                
                for word in words:
                    bdd.insert(sql_insert_word, (
                        word,
                        place.id
                    ))
                print("[",*words, "] inserted")
        except:
            print("error: unknown")

    def on_error(self, status):
        return False


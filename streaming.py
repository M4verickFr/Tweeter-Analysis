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

if __name__ == '__main__':
    sql_insert_city = "INSERT INTO `city`(`place_id`, `display_name`, `polygon`, `lat`, `lon`) VALUES (%s,%s,%s,%s,%s)"
    sql_insert_tweet = "INSERT INTO `tweet`(`id_tweet`, `created_at`, `full_text`, `lang`, `retweet_count`, `latitude`, `longitude`, `id_city`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"      
    sql_insert_word = "INSERT INTO `word`(`word`, `id_city`) VALUES (%s,%s)"
    
    bdd = database("localhost","root","","twitter")
    bdd.connect()
    
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth, wait_on_rate_limit=True)

    location = [-5.225, 41.333, 9.55, 51.2]
    track = ['France','Polytech','Ocean','Ville','Ecole','Ingenieur','Annecy','Voyage','openstreetmap'
             'Grenoble','Paris','Lyon','ia','adwords','RGPD','CNIL','Cookie','Instagram','GoogleMaps']
    languages = ['fr']
    dictonnary = enchant.Dict("fr_FR")
    
    toknizer = RegexpTokenizer(r'''\w'|\w+|[^\w\s]''')

    stream = Stream(auth, listener, tweet_mode='extended')
    stream.filter(locations=location,languages=languages,track=track)
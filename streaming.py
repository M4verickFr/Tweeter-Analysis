import json
from geopy.geocoders import Nominatim, Photon
from tweepy import OAuthHandler, Stream, StreamListener

from database import database
from keys import *

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, raw_data):
        self.process_data(raw_data)
        return True

    def process_data(self, raw_data):
        tweet = json.loads(raw_data)
        
        city = geolocator.geocode(tweet["user"]["location"], language='fr', osm_tag=["place:city","place:town"])
            
        if not city:
            print("error")
            return

        print(tweet["text"])
        
        if bdd.request_fetchone(f"SELECT COUNT(*) FROM city WHERE osm_id={city.raw['properties']['osm_id']}") == 0:
            bdd.insert(sql_insert_city, (city.raw['properties']["osm_id"],
                city.address,
                str(city.latitude)[:20],
                str(city.longitude)[:20]
            ))
            print(f"inserted: city-{city.raw['properties']['osm_id']}")
        
        bdd.insert(sql_insert_tweet, (tweet["id_str"], 
            tweet["created_at"], 
            tweet["text"], tweet["lang"], 
            tweet["retweet_count"]
        ))
        print(f"inserted: tweet-{tweet['id_str']}")


    def on_error(self, status):
        return False

if __name__ == '__main__':
    sql_insert_tweet = "INSERT INTO `tweet`(`id_tweet`, `created_at`, `full_text`, `lang`, `retweet_count`) VALUES (%s,%s,%s,%s,%s)"  
    sql_insert_city = "INSERT INTO `city`(`osm_id`, `display_name`, `lat`, `lon`) VALUES (%s,%s,%s,%s)"
    sql_insert_word = "INSERT INTO `city`(`word`, `id_city`) VALUES (%s,%s)"
    bdd = database("localhost","root","","twitter")
    bdd.connect()
    
    geolocator = Nominatim(user_agent="http")
    geolocator = Photon(user_agent="http")
    
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener, tweet_mode='extended')
    # stream.filter(locations=[6.0484121,45.8280024,6.2043932,45.9766928]) #France, Annecy
    # stream.filter(locations=[5.6776059,45.1541442,5.7531176,45.2140762]) # France, Grenoble
    stream.filter(locations=[-4.82,42.49,8.05,51.07], languages=["fr", "en"]) # France

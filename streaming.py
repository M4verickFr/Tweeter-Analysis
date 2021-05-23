# Externe import
import json
from tokenization import tokenize
from tweepy import OAuthHandler, Stream, StreamListener, API

# Interne import
import credentials
from database import database
from models.City import City
from models.Tweet import Tweet

class TwitterClient():
    def __init__(self, credentials, listener):
        self.auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        self.auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        
        self.api = API(self.auth, wait_on_rate_limit=True)
        self.listener = listener
        
    def get_api(self):
        return self.api
        
    def stream(self, locations=None, languages=None, track=None):
        stream = Stream(self.auth, self.listener, tweet_mode='extended')
        stream.filter(locations=location,languages=languages,track=track)

class StdOutListener(StreamListener):
    """Listener to manipulate tweet and insert it in database 

    Args:
        StreamListener (Listener): StdOutListener extends default StreamListener
    """
    
    def on_data(self, raw_data):
        """Method executed when a tweet listens

        Args:
            raw_data (str): tweet informations
        """
        try: 
            tweet = json.loads(raw_data)

            if tweet['geo']: # If the tweet has geographical information
                
                # Find the nearest city
                lat, lon = tweet["geo"]["coordinates"]
                places = tw_client.get_api().reverse_geocode(lat, lon, max_result=1, granularity="city")
                
                if (len(places) == 0):
                    print("error: locations not find")
                    return
                
                # Insert city in the database if it is not already inserted
                if not City.exist(bdd, places[0].id):
                    City.insert(bdd, places[0])
                    print("city inserted")
                
                # Insert tweet in the database
                Tweet.insert(bdd, tweet, places[0].id)
                print("tweet inserted")
                
                # Tokenize tweet
                tokenize(bdd, tweet, places[0].id)
        except:
            print("error: unknown")
        

if __name__ == '__main__':
    # Setup mysql.connector to authenticate to database
    bdd = database("localhost","root","","twitter")
    bdd.connect()
    
    # Define variables to filter the stream
    location = [-5.225, 41.333, 9.55, 51.2]
    languages = ['fr']
    
    # Define twitter client, and call stream method to start streaming
    tw_client = TwitterClient(credentials, StdOutListener())
    tw_client.stream(locations=location,languages=languages)
class Tweet(object):
    def __init__(self, id, id_tweet, created_at, full_text, lang, retweet_count, latitude, longitude, id_city):
        self.id = id
        self.id_tweet = id_tweet
        self.created_at = created_at
        self.full_text = full_text
        self.lang = lang
        self.retweet_count = retweet_count
        self.latitude = latitude
        self.longitude = longitude
        self.id_city = id_city
        

    @staticmethod
    def insert(bdd, tweet, id_city):
        if ("extended_tweet" in tweet):
            text = tweet["extended_tweet"]["full_text"]
        else:
            text = tweet["text"]
            
        bdd.insert("tweet", {
            "id_tweet": tweet["id_str"],
            "created_at": tweet["created_at"], 
            "full_text": text, 
            "lang": tweet["lang"], 
            "retweet_count": tweet["retweet_count"],
            "latitude": tweet["geo"]["coordinates"][0],
            "longitude": tweet["geo"]["coordinates"][1],
            "id_city": id_city
        })
import sys
import tweepy
import mysql.connector

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '2468106715-DV5ofXwJA1sn4SK6Po5Bq3LMrBZH4pndKUUGIdS'
ACCESS_SECRET = '6WIrWyYDYeADHUA5IsTApjpya28kDYrm5FTIxiJ19zuCq'
CONSUMER_KEY = 'pcKVYLjgUiKMIyHWURiFQlTQ4'
CONSUMER_SECRET = 'scKHTKQtB7GOqw9B8cuERkmEgZqKyOFlH9y9wPH8PP3oM2shVp'

# Variables for search tweets
key_words = ["ia", "adwords", "RGPD", "CNIL", "Cookie"]
geocodes = ["45.899247,6.129384,50km", "48.856614,2.352222,50km", "45.764043,4.835659,50km"]

# Setup tweepy to authenticate with Twitter credentials:
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

# Setup mysql.connector to authenticate to database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="twitter",
  charset="utf8mb4"
)
cursor = db.cursor()

if len(sys.argv) < 2:
    cursor.execute("SELECT COUNT(*) FROM tweet")
    print(f"tweetNumber : {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM tweet WHERE latitude != ''")
    print(f"coordinatesNumber : {cursor.fetchone()[0]}")
    
    sys.exit(0)

if  sys.argv[1] == "load_tweet":
    for key_word in key_words:
        for geocode in geocodes:  
            fetched_tweets = api.search(q=key_word,count=100, tweet_mode="extended", lang="fr", geocode=geocode)
            
            print(key_word + " - " + str(len(fetched_tweets)))
            
            for tweet in fetched_tweets:
                try:
                    if tweet.geo == None:
                        sql = "INSERT INTO `tweet`(`id_tweet`, `created_at`, `full_text`, `lang`, `retweet_count`) VALUES (%s,%s,%s,%s,%s)"
                        cursor.execute(sql, (tweet.id_str, tweet.created_at, tweet.full_text, tweet.lang, tweet.retweet_count))
                    else:
                        sql = "INSERT INTO `tweet`(`id_tweet`, `created_at`, `full_text`, `lang`, `retweet_count`, `latitude`, `longitude`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sql, (tweet.id_str, tweet.created_at, tweet.full_text, tweet.lang, tweet.retweet_count, tweet.geo["coordinates"][0], tweet.geo["coordinates"][1]))
                except:
                    print("error")
                    print(tweet._json)

    db.commit()
    print("Loading tweets...")
    sys.exit(0)
    
if  sys.argv[1] == "delete_tweet":
    sql = "DELETE FROM tweet"
    cursor.execute(sql)
    db.commit()
    print("Deleting all tweets...")
    sys.exit(0)
    
print("error : use twitter_search.py load_tweet or twitter_search.py delete_tweet")
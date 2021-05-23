import enchant
from nltk import RegexpTokenizer
from nltk.corpus import stopwords

from models.Word import Word

dictonnary = enchant.Dict("fr_FR")
toknizer = RegexpTokenizer(r'''\w'|\w+|[^\w\s]''')

def tokenize(bdd,tweet,id_city):
    """Retrieves words in tweet and inserts them into the database

    Args:
        bdd (database): object to connect to database
        tweet (dict): The tweet and this information
        id_city (str): Nearest city to the tweet 
    """
    words = toknizer.tokenize(tweet["extended_tweet"]["full_text"] if "extended_tweet" in tweet else tweet["text"])
    words = list(filter(lambda word: len(word) > 2 and "@" not in word and word[:5] != "https" and word not in stopwords.words('french') and dictonnary.check(word), words))
    
    for w in words:
        Word.insert(bdd, w, id_city)
        
    print(f"{len(words)} words inserted")
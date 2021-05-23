class Word(object):
    def __init__(self, id, word, id_city):
        self.id = id
        self.word = word
        self.id_city = id_city

    @staticmethod
    def insert(bdd, word, id_city):            
        bdd.insert("word", {
            "word": word,
            "id_city": id_city
        })
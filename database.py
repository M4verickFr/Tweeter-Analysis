import mysql.connector
from mysql.connector import cursor

class database():
    def __init__(self, host, user, password, database, charset='utf8mb4'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        
    def connect(self):
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset
        )
        self.cursor = self.db.cursor()
        
    def insert(self, sql, data):
        self.cursor.execute(sql, data)
        self.db.commit()
        
    def request(self, sql):
        self.cursor.execute(sql)
        self.db.commit()
        
    def request_fetchall(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def request_fetchone(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]
import mysql.connector

class database():
    def __init__(self, host, user, password, database, charset='utf8mb4'):
        """Constructor use to create database object

        Args:
            host (str): database ip / url
            user (str): username for connection
            password (str): password for connection
            database (str): name of database
            charset (str, optional): charset of data. Defaults to 'utf8mb4'.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        
    def connect(self):
        """connect database object to mysql database
        """
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset
        )
        self.cursor = self.db.cursor()
        
    def insert(self, table, data):
        """Insert the data in the table of the database 

        Args:
            table (str): Table where the data is inserted.
            data (dict): Data to insert
        """
        sql = f"insert into `{table}`(`"
        sql += "`, `".join(data.keys())
        sql += "`) VALUES ("+("%s,"*len(data.values()))[:-1]
        sql += ")"
        
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()

    def request_fetchall(self, sql):
        """Get all elements of request

        Args:
            sql (str): Sql request

        Returns:
            Array: All elements returned by request
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def request_fetchone(self, sql):
        """Get first element of request

        Args:
            sql (str): Sql request

        Returns:
            dict: data of first element
        """
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]
    
    def get_all(self, table):
        """Get all element in table

        Args:
            table (str): Database table name

        Returns:
            Array: All elements returned by request
        """
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor.fetchall()
    
    def count(self,table):
        """Get number of elements in table

        Args:
            table (str): Database table name

        Returns:
            int: Number of elements in table
        """
        return self.request_fetchone(f"SELECT COUNT(*) FROM {table}")
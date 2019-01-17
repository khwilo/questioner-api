'''Module to setup the database'''
import psycopg2

from instance.config import Config

class DatabaseSetup:
    '''Initiliaza a database connection'''
    def __init__(self):
        self.connection = psycopg2.connect(
            host=Config.DATABASE_HOST,
            dbname=Config.DATABASE_NAME,
            user=Config.DATABASE_USER,
            password=Config.DATABASE_PASSWORD
        )
        self.cursor = self.connection.cursor()

    def initialize_db(self):
        '''Initialize the database'''
        return self.connection

    def initiliaze_database_tables(self):
        '''Create the tables'''
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                firstname VARCHAR(50),
                lastname VARCHAR(50),
                othername VARCHAR(50),
                email VARCHAR(254) UNIQUE NOT NULL,
                phoneNumber VARCHAR(15),
                username VARCHAR(50) UNIQUE NOT NULL,
                registered TIMESTAMP,
                isAdmin BOOLEAN NOT NULL,
                password VARCHAR(100) NOT NULL
            );
            """
        ) # Initiliaze the users table

        self.cursor.close()
        self.connection.commit()
        self.connection.close()

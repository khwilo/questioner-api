'''Module to setup the database'''
import psycopg2

from instance.config import APP_CONFIG

class DatabaseSetup:
    '''Initiliaza a database connection'''
    def __init__(self, config_name):
        self.connection = psycopg2.connect(APP_CONFIG[config_name].DATABASE_CONNECTION_URL)
        self.cursor = self.connection.cursor()

    def initialize_db(self):
        '''Initialize the database'''
        return self.connection

    def database_tables(self):
        '''Create tables queries'''
        user = """
                CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                firstname VARCHAR(50),
                lastname VARCHAR(50),
                othername VARCHAR(50),
                email VARCHAR(254) UNIQUE NOT NULL,
                phoneNumber VARCHAR(15),
                username VARCHAR(50) UNIQUE NOT NULL,
                registered TIMESTAMP NOT NULL,
                isAdmin BOOLEAN NOT NULL,
                password VARCHAR(100) NOT NULL
                )
                """
        table_queries = [user]
        return table_queries

    def create_tables(self):
        '''Create the database tables'''

        table_queries = self.database_tables()

        for table_query in table_queries:
            self.cursor.execute(table_query)
        self.connection.commit()

'''Database configuration file'''
import os
import psycopg2
from flask import current_app

def establish_connection(connect_url):
    '''Establish a database connection'''
    conn = psycopg2.connect(connect_url)
    return conn


def initiate_db():
    '''Initiate the database connection'''
    url = current_app.config['DATABASE_CONNECTION_URL']
    conn = psycopg2.connect(url)
    return conn


def init_test_db():
    '''Initiate the test database'''
    conn = establish_connection(os.getenv('DATABASE_TEST_URL'))
    curr = conn.cursor()
    queries = create_tables()

    for query in queries:
        curr.execute(query)
    conn.commit()
    return conn


def destroy():
    '''Remove the database tables'''
    conn = establish_connection(os.getenv('DATABASE_TEST_URL'))
    curr = conn.cursor()
    users = "DROP TABLE IF EXISTS users CASCADE"
    queries = [users]

    for query in queries:
        curr.execute(query)
    conn.commit()


def create_tables():
    '''Create the database tables'''
    db1 = """CREATE TABLE IF NOT EXISTS users(
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
    );""" # create the users table

    queries = [db1]
    return queries

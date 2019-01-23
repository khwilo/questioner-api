'''Definitions for the database'''
import os
import psycopg2

from flask import current_app

def establish_connection():
    '''Establish a database connection'''
    database_url = current_app.config['DATABASE_URL']
    try:
        connection = psycopg2.connect(database_url)
    except psycopg2.DatabaseError as error:
        print("error {}".format(error))
    return connection

def create_table_queries():
    '''SQL queries to create a database table'''
    users = """CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    othername VARCHAR(50) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    registered TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    password VARCHAR(100) NOT NULL
    )""" # create the users table

    meetup = """CREATE TABLE IF NOT EXISTS meetups(
    id SERIAL PRIMARY KEY,
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    m_location VARCHAR NOT NULL,
    images VARCHAR [] DEFAULT '{}',
    topic VARCHAR NOT NULL,
    m_description VARCHAR(200) NOT NULL,
    happening_on DATE NOT NULL,
    tags VARCHAR [] DEFAULT '{}'
    )""" # create the meetups table

    question = """CREATE TABLE IF NOT EXISTS questions(
    id SERIAL PRIMARY KEY,
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INT NOT NULL,
    meetup_id INT NOT NULL,
    title VARCHAR NOT NULL,
    body VARCHAR NOT NULL,
    votes INT DEFAULT 0,
    FOREIGN KEY (created_by) REFERENCES users (id)  ON DELETE CASCADE,
    FOREIGN KEY (meetup_id) REFERENCES meetups (id) ON DELETE CASCADE
    )""" # create the questions table

    rsvp = """CREATE TABLE IF NOT EXISTS rsvps(
    id SERIAL PRIMARY KEY,
    meetup_id INT NOT NULL,
    user_id INT NOT NULL,
    response VARCHAR NOT NULL,
    FOREIGN KEY (meetup_id) REFERENCES meetups (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )""" # create the rsvps table

    queries = [users, meetup, question, rsvp]
    return queries

def drop_table_queries():
    '''SQL queries to drop tables'''
    drop_queries = [
        "DELETE FROM users WHERE is_admin='f'",
        "DELETE FROM meetups CASCADE",
        "DELETE FROM questions CASCADE",
        "DELETE FROM rsvps CASCADE"
    ]
    return drop_queries

def create_tables(db_connection):
    '''Create the database tables'''
    cursor = db_connection.cursor()
    queries = create_table_queries()
    for query in queries:
        cursor.execute(query)
    db_connection.commit()

def destroy():
    '''Delete database entries'''
    database_url = os.getenv('DATABASE_TEST_URL')
    connection = psycopg2.connect(database_url)
    cursor = connection.cursor()
    queries = drop_table_queries()
    for query in queries:
        cursor.execute(query)
    connection.commit()

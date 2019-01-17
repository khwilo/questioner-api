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
    meetups = "DROP TABLE IF EXISTS meetups CASCADE"
    questions = "DROP TABLE IF EXISTS questions CASCADE"
    rsvps = "DROP TABLE IF EXISTS rsvps CASCADE"
    queries = [users, meetups, questions, rsvps]

    for query in queries:
        curr.execute(query)
    conn.commit()


def create_tables():
    '''Create the database tables'''
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
    password_1 VARCHAR(100) NOT NULL,
    password_2 VARCHAR(100) NOT NULL
    );""" # create the users table

    meetup = """CREATE TABLE IF NOT EXISTS meetups(
    id SERIAL PRIMARY KEY,
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    m_location VARCHAR NOT NULL,
    images VARCHAR ARRAY NOT NUL,
    topic VARCHAR NOT NULL,
    m_description VARCHAR(200) NOT NULL,
    happening_on DATE NOT NULL,
    tags VARCHAR ARRAY NOT NULL
    );""" # create the meetups table

    question = """CREATE TABLE IF NOT EXISTS questions(
    id SERIAL PRIMARY KEY,
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INT NOT NULL,
    meetup_id INT NOT NULL,
    title VARCHAR NOT NULL,
    body VARCHAR NOT NULL,
    votes INT DEFAULT 0,
    FOREIGN_KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN_KEY (meetup_id) REFERENCES meetups(id) ON DELETE CASCADE
    );""" # create the questions table

    rsvp = """CREATE TABLE IF NOT EXISTS rsvps(
    id SERIAL PRIMARY KEY,
    meetup_id INT NOT NULL,
    user_id INT NOT NULL,
    response VARCHAR NOT NULL,
    FOREIGN_KEY (meetup_id) REFERENCES meetups(id) ON DELETE CASCADE,
    FOREIGN_KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );""" # create the rsvps table

    queries = [users, meetup, question, rsvp]
    return queries

'''Module to define migrations for dev and test db'''
import os
import psycopg2

from app.api.v1.models.user_model import UserModel
from db import create_tables

def migrate_main():
    '''Perform database migrations for the main db'''
    database_url = os.getenv('DATABASE_URL')
    connection = psycopg2.connect(database_url)
    create_tables(connection)
    query = """INSERT INTO users(
    firstname, lastname, othername, email, phone_number, username, is_admin, password) \
    VALUES('Khwilo', 'Kabaka', 'Watai', 'watai@questioner.com', '0700000000', 'watai', True, '{}')"""\
    .format(UserModel.generate_password_hash('questioner_1234'))
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def migrate_test():
    '''Perform database migrations for the test db'''
    database_url = os.getenv('DATABASE_TEST_URL')
    connection = psycopg2.connect(database_url)
    create_tables(connection)
    query = """INSERT INTO users(
    firstname, lastname, othername, email, phone_number, username, is_admin, password) \
    VALUES('Khwilo', 'Kabaka', 'Watai', 'watai@questioner.com', '0700000000', 'watai', True, '{}')"""\
    .format(UserModel.generate_password_hash('questioner_1234'))
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

if __name__ == '__main__':
    migrate_main()
    migrate_test()

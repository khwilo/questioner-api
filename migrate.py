'''Module to define migrations for dev and test db'''
import os
import psycopg2

from app.api.v2.models.user_model import UserModel
from db import create_tables

def migrate(database_url):
    '''Create tables and an admin user'''
    connection = psycopg2.connect(database_url)
    create_tables(connection)
    query = """INSERT INTO users(
    firstname, lastname, othername, email, phone_number, username, is_admin, password) \
    VALUES('Khwilo', 'Kabaka', 'Watai', 'watai@questioner.com', '0700000000', 'watai', True, '{}')"""\
    .format(UserModel.generate_password_hash('questioner_1234'))
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def migrate_main():
    '''Perform database migrations for the main db'''
    migrate(os.getenv('DATABASE_URL'))

def migrate_test():
    '''Perform database migrations for the test db'''
    migrate(os.getenv('DATABASE_TEST_URL'))

if __name__ == '__main__':
    migrate_main()
    migrate_test()

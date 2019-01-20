'''Module to seed the database with an admin user'''
import os
import psycopg2

from db import create_tables, create_admin

def migrate_main():
    '''Perform database migrations for the main db'''
    database_url = os.getenv('DATABASE_URL')
    connection = psycopg2.connect(database_url)
    create_tables(connection)
    create_admin(connection)

def migrate_test():
    '''Perform database migrations for the test db'''
    database_url = os.getenv('DATABASE_TEST_URL')
    connection = psycopg2.connect(database_url)
    create_tables(connection)
    create_admin(connection)

if __name__ == '__main__':
    # migrate_main()
    migrate_test()

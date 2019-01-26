"""Definitions for development and testing environment migrations"""
import os
import psycopg2

from app.api.v2.models.user_model import UserModel
from db import create_tables, destroy

def migrate(database_url):
    """Create tables and an admin user"""
    connection = psycopg2.connect(database_url)
    create_tables(connection)
    query = """INSERT INTO users(
    firstname, lastname, othername, email, phone_number, username, is_admin, password) \
    VALUES('Khwilo', 'Kabaka', 'Watai', 'watai@questioner.com', '0700000000', 'watai', True, '{}')"""\
    .format(UserModel.generate_password_hash('questioner_1234'))
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def migrate_dev():
    """Perform database migrations for the development database"""
    migrate(os.getenv('DATABASE_URL'))

def drop_dev():
    """Drop the development database tables"""
    destroy(os.getenv('DATABASE_URL'))

def migrate_test():
    """Perform database migrations for the testing database"""
    migrate(os.getenv('DATABASE_TEST_URL'))

if __name__ == '__main__':
    drop_dev()
    migrate_dev()

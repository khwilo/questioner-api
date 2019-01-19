"""Module representing a user entity"""
from datetime import datetime

from app.api.v2.models.database import DatabaseSetup

class UserModel:
    """Entity representation for a user"""
    def __init__(self, **kwargs):
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.othername = kwargs.get('othername')
        self.email = kwargs.get('email')
        self.phone_number = kwargs.get('phone_number')
        self.username = kwargs.get('username')
        self.registered = str(datetime.utcnow())
        self.is_admin = kwargs.get('is_admin')
        self.password = kwargs.get('password')
        self.database = DatabaseSetup.initialize_db()

    def add_user(self):
        """Add a new user to the 'users' table"""
        query = """INSERT INTO users(
        firstname, lastname, othername, email, phone_number, username, is_admin, password) VALUES(
        '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(
            self.firstname,
            self.lastname,
            self.othername,
            self.email,
            self.phone_number,
            self.username,
            self.is_admin,
            self.password)
        self.database.cursor().execute(query)
        self.database.commit()
        self.database.cursor().close()

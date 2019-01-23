'''Module containing sample data for testing'''
USER_REGISTRATION = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="tester@example.com",
    phoneNumber="0700000000",
    username="tester_user",
    password="12345"
)

USER_DUPLICATE_USERNAME = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="test@example.com",
    phoneNumber="0700000000",
    username="tester_user",
    password="12345"
)

USER_DUPLICATE_EMAIL = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="tester@example.com",
    phoneNumber="0700000000",
    username="tes_user",
    password="12345"
)

USER_DIGIT_USERNAME = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="test@example.com",
    phoneNumber="0700000000",
    username="1234",
    password="12345"
)

USER_EMPTY_USERNAME = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="test@example.com",
    phoneNumber="0700000000",
    username="",
    password="12345"
)

USER_EMPTY_PASSWORD = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="test@example.com",
    phoneNumber="0700000000",
    username="test_user",
    password=""
)

USER_WRONG_EMAIL_FORMAT = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="testexample.com",
    phoneNumber="0700000000",
    username="test",
    password="12345"
)

USER_LOGIN = dict(username="tester_user", password="12345")

ADMIN_LOGIN = dict(username="watai", password="questioner_1234")

USER_LOGIN_INCORRECT_PASSWORD = dict(username="tester_user", password="abcde")

MEETUP = dict(
    location="Test Location",
    images='{image1, image2}',
    topic="Test Topic",
    description="Test description",
    happeningOn="Jan 10 2019 3:30PM",
    tags='{programming, design}'
)

NEW_MEETUP = dict(
    location="Test New Location",
    images='{}',
    topic="Test New Topic",
    happeningOn="Mar 5 2019 11:00AM",
    tags='{Programming, Design}'
)

QUESTION = dict(
    title="test title",
    body="test body"
)

RSVP = dict(response="maybe")

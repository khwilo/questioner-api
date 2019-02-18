'''Module containing sample data for testing'''
USER_REGISTRATION = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="tester@example.com",
    phoneNumber="071-123-4567",
    username="tester_user",
    password="12345abcsde"
)

NEW_USER_REGISTRATION = dict(
    firstname="test_first new",
    lastname="test_last new",
    othername="test_other new",
    email="testernew@example.com",
    phoneNumber="072-345-6789",
    username="tester_user_new",
    password="abcdqwqs11234"
)

USER_DUPLICATE_USERNAME = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="test@example.com",
    phoneNumber="073-456-7890",
    username="tester_user",
    password="12345abcsde"
)

USER_DUPLICATE_EMAIL = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="tester@example.com",
    phoneNumber="074-567-8901",
    username="tes_user",
    password="12345abcsde"
)

USER_DIGIT_USERNAME = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="test@example.com",
    phoneNumber="075-678-9012",
    username="1234",
    password="12345abcsde"
)

USER_EMPTY_USERNAME = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="test@example.com",
    phoneNumber="076-789-0123",
    username="",
    password="12345abcsde"
)

USER_EMPTY_PASSWORD = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="test@example.com",
    phoneNumber="077-890-1234",
    username="test_user",
    password=""
)

USER_WRONG_EMAIL_FORMAT = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="testexample.com",
    phoneNumber="078-901-2345",
    username="test",
    password="12345abcsde"
)

USER_WRONG_PHONE_FORMAT = dict(
    firstname="test_first",
    lastname="test_last",
    othername="test_other",
    email="test@example.com",
    phoneNumber="0789012345",
    username="test",
    password="12345abcsde"
)

USER_LOGIN = dict(username="tester_user", password="12345abcsde")

NEW_USER_LOGIN = dict(username="tester_user_new", password="abcdqwqs11234")

ADMIN_LOGIN = dict(username="watai", password="questioner_1234")

USER_LOGIN_INCORRECT_PASSWORD = dict(username="tester_user", password="abcde122edasda")

MEETUP = dict(
    location="PAC",
    images='{image1, image2}',
    topic="Test Topic",
    description="Test description",
    happeningOn="Jan 10 2019, 3:30 PM",
    tags='{programming, design}'
)

NEW_MEETUP = dict(
    location="Andela",
    images='{image3, image4}',
    topic="Test Topic Two",
    description="Test description Two",
    happeningOn="Mar 5 2019, 11:00 PM",
    tags='{Art, Entertainment}'
)

QUESTION = dict(
    title="test title",
    body="test body"
)

RSVP = dict(response="maybe")

COMMENT = dict(comment="Test comment")

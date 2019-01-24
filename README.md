# QUESTIONER API

[![Build Status](https://travis-ci.org/khwilo/questioner-api.svg?branch=develop)](https://travis-ci.org/khwilo/questioner-api) [![Coverage Status](https://coveralls.io/repos/github/khwilo/questioner-api/badge.svg?branch=develop)](https://coveralls.io/github/khwilo/questioner-api?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/83bc5cc4ff739b5841c1/maintainability)](https://codeclimate.com/github/khwilo/questioner-api/maintainability)

## DESCRIPTION

API implementation for the [Questioner](https://khwilo.github.io/questioner/) application.

## Work In Progress

- [x] User registration
- [x] User log in
- [ ] User log out
- [x] Admin user creating a meetup
- [x] Fetching all meetups
- [x] Fetching a specific meetup
- [x] Admin user deleting a meetup
- [x] User posting a question
- [x] User commenting on a question
- [ ] User upvoting on a question
- [ ] User downvoting on a question
- [ ] User RSVP meetup

### API ENDPOINTS

**_NOTE_**:

- API endpoints are prefixed by `/api/v2`.
- Fields for the date are specified like this `month day year time`. An example date format: `"Jan 10 2019 12:15AM"`

| Method        | Endpoint                                                       | Description              |
| ------------- | -------------------------------------------------------------- | ------------------------ |
| POST          | `/auth/signup`                                                 | Create a user record     |
| POST          | `/auth/login`                                                  | Log in a user            |
| POST          | `/meetups`                                                     | Create a meetup record   |
| GET           | `/meetups/<meetup-id>`                                         | Fetch a specific meetup record |
| GET           | `/meetups/upcoming/`                                           | Fetch all upcoming meetup records |
| POST          | `/meetups/<meetup-id>/questions`                               | Create a question for a specific meetup |
| PATCH         | `/meetups/<meetup-id>/questions/<question-id>/upvote`          | Upvote (_increase votes by 1_) a specific question |
| PATCH         | `/meetups/<meetup-id>/questions/<question-id>/downvote`        | Downvote (_decrease votes by 1_) a specific question |
| POST          | `/meetups/<meetup-id>/rsvps`                                   | Respond to meetup RSVP with a "yes", "no" or "maybe" |

## Pre-requisites

Make sure you have Python version 3 and Postgres installed on your local machine.

## Usage

1. Clone the repository using the command:

    ```bash
    $ git clone https://github.com/khwilo/questioner-api.git
    ``` 

2. Change directory to the location you cloned the repository:

    ```bash
    $ cd questioner-api
    ``` 

3. Set environment variables for **APP_SETTINGS**, **SECRET_KEY**, **JWT_SECRET_KEY**, **DATABASE_URL** and **DATABASE_TEST_URL**. For more information see the `config.py` file from the _instance_ directory.

4. Create a database for the development database and test environment, example:

    ```bash
    $ sudo -u postgres psql
    $ CREATE DATABASE yourdbname;
    $ CREATE USER youruser WITH ENCRYPTED PASSWORD 'yourpassword';
    $ GRANT ALL PRIVILEGES ON DATABASE yourdbname TO youruser;
    ``` 

4. Create a virtual environment and activate it:

    ```bash
    $ python3 -m venv venv
    $ source venv/bin/activate
    ``` 

5. Install the required dependencies:

    ```bash
    $ pip install -r requirements.txt
    ``` 

6. Create the tables by running this script:

    ```bash
    $ python3 migrate.py
    ```

7. Run the Flask application:

    ```bash
    $ export FLASK_APP=run.py
    $ flask run
    ``` 

### Test the API on Postman

- The accepted content type header is as follows:

  - *key*: **Content-Type** 
  - *value*: **application/json**

- Authorization header is as follows:

  - *key*: **Authorization** 
  - *value*: **Bearer** `<access-token>`

The **access-token** is found from the response when a user logs in.

### Unit testing

Running the unit test is done using the command `pytest --cov=app/api` or `python -m unittest discover -v` on your terminal.

## Heroku

The API is hosted on Heroku at `https://q-questioner-api.herokuapp.com/`. Currently there is no default route that is configured but you can test the API endpoints by providing their paths after the host name. For example, to test user account creation use the URL `https://q-questioner-api.herokuapp.com/auth/register`.

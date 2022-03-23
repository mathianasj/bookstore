# Book Store API
A basic book store application that allows you to view books and their availability with the addition to check out/in them.  This is a completely open api with no authentication or authorization, this is done intentionally to utilize something like an envoy proxy and combination of decoupled authorization such as Open Policy Agent.

## Running Locally
The easiest way to get started locally is to setup a virtualenv environment in this base and utilize the requirements file to install the required dependencies.  This guide assumes the installation of python3, pip3, and virtualenv.  This application utilizes a postgres database to store the data for the end points.  There is a provided docker compose to run the database server if you do not have one currently configured.

### Running Server Dependencies
You will need to run this in a separate terminal window from the remaining commands
1. `docker-compose up`

### Configure Virtualenv
Run the following set of commands to get your venv setup
1. `virtualenv -p python3 venv`
1. `source ./venv/bin/activate`
1. `pip install -r requirements.txt`

### Run the development server
To run the development server you'll first need to run the migration scripts to setup the database, and then run the actual django server.

1. `python manage.py migrate`
    1. This only needs run the first time or when changes are made to the models which would affect the database schema
1. `python manage.py runserver`
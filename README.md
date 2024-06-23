# SPLIEWISE APP

## Project Overview

Splitwise is a versatile expense tracking and splitting application designed to help users manage and split expenses effortlessly with friends, family, roommates, or colleagues. It is ideal for situations like group trips, shared living arrangements, or joint financial activities. Here's an overview of the app's features and functionalities.


## Setting up Environment Variables
Ensure that you have the necessary environment variables set. Create a `.env` file in the root directory of the project and include the following:

- DB_NAME=''
- DB_USER=''
- DB_PASSWORD=''
- DB_HOST=''
- DB_PORT=''


## Project Setup

python version = 3.9

1. Create virtual-environment 
    - If virtualenv is installed
        - virtualenv -p python(your python version) environment-name
    - If virtualenv is not installed, install this using `pip install virtualenv`

2. Activate Virtualenv
    - source environment-name/bin/activate

3. Install requirements.txt
    - pip3 install -r requirements.txt

4. Run migration and migrate command:
    - python manage.py makemigrations
    - python manage.py migrate
    - Create super user for admin panel by filling required details
        - python manage.py createsuperuser

5. Run Project Using - `python manage.py runserver`


## Project Setup with Docker

1. `sudo docker-compose build`
2. `sudo docker-compose up`

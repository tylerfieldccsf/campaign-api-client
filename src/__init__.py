import json
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('../logs/log.txt', 'a')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

with open('../resources/config.json', 'r') as f:
    config = json.load(f)

# Variables below are set in resources/config.json file
# TEST or LIVE
env = 'TEST'

# Base URL of the API. Example - "https://netfile.com/filing/api"
api_url = config[env]['API_URL']
# Username credential to authenticate against the Campaign API
api_key = config[env]['API_KEY']
# Password credential to authenticate against the Campaign API
api_password = config[env]['API_PASSWORD']
# Name of host to connect to PostgreSQL database
db_host = config[env]['HOST']
# Postgres database to connect to
db_name = config[env]['DB_NAME']
# Postgres database username
db_user = config[env]['DB_USER']
# Postgres database password
db_password = config[env]['DB_PASSWORD']

# Unit Test values
db_host_unit_test = 'localhost'
db_name_unit_test = config['TEST']['DB_NAME']
db_user_unit_test = config['TEST']['DB_USER']
db_password_unit_test = config['TEST']['DB_PASSWORD']

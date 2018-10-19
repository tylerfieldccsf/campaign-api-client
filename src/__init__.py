# TODO - Update this example from requests library to be NetFile specific
#       This example uses a Python Test style that is embedded in documentation, which is
#       detected by interpreter and executed. Not sure if I should use this or not, but the
#       requests project does, so it's worth looking into
"""
Campaign API Sync Library
~~~~~~~~~~~~~~~~~~~~~

Campaign API Sync is a library.

usage:

#    >>> import src
#    >>> r = requests.get('https://www.python.org')
#    >>> r.status_code
#    200
#    >>> 'Python is a programming language' in r.content
#    True
#
# ... or POST:
#
#    >>> payload = dict(key1='value1', key2='value2')
#    >>> r = requests.post('http://httpbin.org/post', data=payload)
#    >>> print(r.text)
   {
     ...
     "form": {
       "key2": "value2",
       "key1": "value1"
     },
     ...
   }

:copyright: (c) 2018
:license:
"""

import json
from campaign_api_repository import CampaignApiRepository
from feed import *
from subscription import *
from session import *
from filing import *
import logging


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('../logs/log.txt', 'a')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

with open('../resources/config.json', 'r') as f:
    config = json.load(f)

# Variables below are set in resources/config.json file
# TEST or PRODUCTION
env = 'TEST'

# Base URL of the API. Example - "https://netfile.com/filing/api"
api_url = config[env]['API_URL']
# Username credential to authenticate against the Campaign API
api_user = config[env]['API_USER']
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

# TODO - Maybe add Debug specific logging configuration here and use that in Unit tests so that we don't get test stuff written to our non-test log file

#
# def sync_filings():
#     """This will allow us to run CampaignApiHttpClient"""
#     logger.debug('Filings sync has started...')

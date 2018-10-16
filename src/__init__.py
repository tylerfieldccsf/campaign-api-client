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
from topics import *
import logging


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('../logs/log.txt', 'a')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

#
# def sync_filings():
#     """This will allow us to run CampaignApiHttpClient"""
#     logger.debug('Filings sync has started...')
#
#     with open('../resources/config.json', 'r') as f:
#         config = json.load(f)
#
#     env = "PRODUCTION"
#     api_url_arg = config[env]['API_URL']
#     api_user_arg = config[env]['API_USER']
#     api_password_arg = config[env]['API_PASSWORD']
#     db_host_arg = config[env]['HOST']
#     db_name_arg = config[env]['DB_NAME']
#     db_user_arg = config[env]['DB_USER']
#     db_password_arg = config[env]['DB_PASSWORD']
#     api_client = CampaignApiHttpClient(api_url_arg, api_user_arg, api_password_arg, db_host_arg, db_name_arg, db_user_arg,
#                                    db_password_arg)
#     api_client.main()

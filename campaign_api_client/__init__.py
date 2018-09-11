# TODO - Update this example from requests library to be NetFile specific
#       This example uses a Python Test style that is embedded in documentation, which is
#       detected by interpreter and executed. Not sure if I should use this or not, but the
#       requests project does, so it's worth looking into
"""
Campaign API Sync Library
~~~~~~~~~~~~~~~~~~~~~

Campaign API Sync is a library.

usage:

#    >>> import requests
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

import logging
from .campaign_api_http_client import *
from .exceptions import *

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('./logs/log.txt', 'a')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)
logger.debug('often makes a very good meal of %s', 'visiting tourists')


def sync_filings():
    logger.debug('Filings sync has started...')

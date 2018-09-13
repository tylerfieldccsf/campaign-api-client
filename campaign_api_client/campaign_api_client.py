#!/usr/bin/python

import requests
import logging
import json
from db_util import PostgresDbUtil
from feed import *
from subscription import *
from session import *
from models import *


class CampaignApiClient:
    """Provides support for synchronizing local database with Campaign API filing data"""

    def __init__(self, base_url, db_host, db_name, db_user, db_password):
        self.headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": "Basic ZGV2QG5ldGZpbGUuY29tOnBhc3N3b3JkOTk="
        }
        self.base_url = base_url
        self.postgres_util = PostgresDbUtil(db_host, db_name, db_user, db_password)

    def fetch_system_report(self):
        url = self.base_url + Routes.SYSTEM_REPORT
        response = requests.get(url, headers=self.headers)
        name = response.json()['name']
        general_status = response.json()['generalStatus']
        components = response.json()['components']
        system_report = SystemReport(name, general_status, components)
        logging.debug('General Status: %s', system_report.general_status)
        logging.debug('General Status: %s', system_report.name)
        for component in system_report.components:
            logging.debug('\tComponent Name: %s', component.name)
            logging.debug('\tComponent Message: %s', component.message)
            logging.debug('\tComponent status: %s', component.status)
            logging.debug('\tComponent Build DateTime: %s', component.build_date_time)
            logging.debug('\tComponent Build Version: %s', component.build_version)
        return system_report

    def create_subscription(self, feed_id, name):
        url = self.base_url + Routes.SYNC_SUBSCRIPTIONS
        body = {
            'feedId': feed_id,
            'name': name
        }
        sub_response = self.post_http_request(url, self.headers, body)
        sub = sub_response['subscription']
        return SyncSubscription(sub['id'], sub['version'], sub['identityId'], sub['feedId'], sub['name'],
                                sub['autoComplete'],
                                sub['status'], sub['filters'])

    def create_session(self, subscription_id):
        url = self.base_url + Routes.SYNC_SESSIONS
        body = {
            'subscriptionId': subscription_id
        }
        session_reponse = self.post_http_request(url, self.headers, body)
        session = session_reponse['session']
        return SyncSession(session['id'], session['version'], session['subscriptionId'], session['identityId'],
                           session['autoComplete'], session['status'], session['sequenceRangeBegin'],
                           session['sequenceRangeEnd'], session['dateRangeBegin'], session['dateRangeEnd'],
                           session['startedAt'], session['endedAt'], session['reads'])

    def end_session(self, session_id):
        pass

    def fetch_sync_topic(self, session_id, topic):
        url = f'{self.base_url}/{Routes.SYNC_SESSIONS}/{session_id}/{topic}'
        response = requests.get(url, headers=self.headers)
        qr = response.json()
        return ListQueryResult(qr['results'], qr['offset'], qr['hasPreviousPage'], qr['hasNextPage'], qr['limit'],
                               qr['totalCount'], qr['empty'], qr['count'], qr['pageNumber'])

    def retrieve_sync_feed(self):
        url = self.base_url + Routes.SYNC_FEED
        response = requests.get(url, headers=self.headers)
        feed = response.json()
        return SyncFeed(feed['id'], feed['version'], feed['productType'], feed['apiVersion'], feed['name'],
                        feed['description'], feed['status'], feed['topics'])

    def create_database_schema(self):
        self.postgres_util.rebuild_schema()

    def post_http_request(self, url, headers, body=None):
        response = requests.post(url, data=json.dumps(body), headers=headers)
        if response.status_code not in [200, 201]:
            raise Exception(f'Error requesting Url: {url}, Response code: {response.status_code}')
        return response.json()

    def main(self):
        try:
            # Build SQL DB
            # self.create_database_schema()

            # Verify the system is ready
            sys_report = self.fetch_system_report()
            if sys_report.general_status == 'Ready':
                logging.info("Campaign API Sync is Ready")

                # Retrieve available SyncFeeds
                feed = self.retrieve_sync_feed()
                logging.info(feed)

                # Create SyncSubscription or use existing SyncSubscription with feed specified
                subscription = self.create_subscription(feed.id, "Feed_1")
                logging.info(subscription)

                # Create SyncSession with SyncSubscription ID specified
                sync_session = self.create_session(subscription.id)
                logging.info(sync_session)

                # Read FilingActivities Topic and persist results
                activities_qr = self.fetch_sync_topic(sync_session.id, "activities")
                logging.info(activities_qr)
                for a in activities_qr.results:
                    activity = FilingActivityV1(a['id'], a['version'], a['creationDate'], a['lastUpdate'], a['activityType'],
                                     a['filingSpecificationKey'], a['origin'], a['originFilingId'], a['agencyId'],
                                     a['applyToFilingId'], a['publishSequence'])
                    self.postgres_util.save_filing_activity(activity)

                # Read FilingElements Topic and persist results
                elements_qr = self.fetch_sync_topic(sync_session.id, "elements")
                logging.info(elements_qr)
                for e in elements_qr.results:
                    element = FilingElementV1(e['id'], e['creationDate'], e['activityId'], e['activityType'],
                                              e['filingSpecificationKey'], e['origin'], e['originFilingId'],
                                              e['agencyId'], e['applyToFilingId'], e['publishSequence'],
                                              e['elementSpecification'], e['elementIndex'], json.dumps(e['modelJson']))
                    self.postgres_util.save_filing_element(element)
            else:
                logging.info("The Campaign API system status is %s and is not Ready", sys_report.general_status)
        except Exception as ex:
            logging.info("The Campaign API system is not Ready. Error message is: ", ex)


class Routes:
    SYSTEM_REPORT = "/system"
    SYNC = "/v1/sync"
    SYNC_FEED = "/v1/sync/feed"
    SYNC_SUBSCRIPTIONS = "/v1/sync/subscriptions"
    SYNC_SESSIONS = "/v1/sync/sessions"


if __name__ == '__main__':
    logger = logging.getLogger()
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('./logs/log.txt', 'a')
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    with open('../resources/config.json', 'r') as f:
        config = json.load(f)

    env = "DEV"
    api_url_arg = config[env]['API_URL']
    db_host_arg = config[env]['HOST']
    db_name_arg = config[env]['DB_NAME']
    db_user_arg = config[env]['DB_USER']
    db_password_arg = config[env]['DB_PASSWORD']
    CampaignApiClient(api_url_arg, db_host_arg, db_name_arg, db_user_arg, db_password_arg).main()

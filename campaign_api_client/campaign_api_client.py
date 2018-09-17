#!/usr/bin/python

import requests
import logging
import json
from campaign_api_repository import CampaignApiRepository
from feed import *
from subscription import *
from session import *
from topics import *


class Routes:
    SYSTEM_REPORT = "/system"
    SYNC = "/v1/sync"
    SYNC_FEED = "/v1/sync/feed"
    SYNC_SUBSCRIPTIONS = "/v1/sync/subscriptions"
    SYNC_SESSIONS = "/v1/sync/sessions"
    SYNC_SESSION_COMMAND = "/v1/sync/sessions/%s/commands/%s"
    SYNC_SUBSCRIPTION_COMMAND = "/v1/sync/subscriptions/%s/commands/%s"


class CampaignApiClient:
    """Provides support for synchronizing local database with Campaign API filing data"""

    def __init__(self, base_url, api_user, api_password, db_host, db_name, db_user, db_password):
        self.headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        self.base_url = base_url
        self.user = api_user
        self.password = api_password
        self.repository = CampaignApiRepository(db_host, db_name, db_user, db_password)

    def fetch_system_report(self):
        url = self.base_url + Routes.SYSTEM_REPORT
        sr = self.get_http_request(url)
        system_report = SystemReport(sr['name'], sr['generalStatus'], sr['components'])
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
        sub_response = self.post_http_request(url, body)
        sub = sub_response['subscription']
        return SyncSubscription(sub['id'], sub['version'], sub['identityId'], sub['feedId'], sub['name'],
                                sub['autoComplete'], sub['status'])

    def execute_subscription_command(self, subscription_id, subscription_version, subscription_command_type):
        ext = Routes.SYNC_SUBSCRIPTION_COMMAND % (subscription_id, subscription_command_type)
        url = self.base_url + ext
        body = {
            'id': subscription_id,
            'version': subscription_version
        }
        self.post_http_request(url, body)

    def create_session(self, subscription_id):
        url = self.base_url + Routes.SYNC_SESSIONS
        body = {
            'subscriptionId': subscription_id
        }
        session_response = self.post_http_request(url, body)
        session = session_response['session']
        return SyncSession(session['id'], session['version'], session['subscriptionId'], session['identityId'],
                           session['autoComplete'], session['status'], session['sequenceRangeBegin'],
                           session['sequenceRangeEnd'], session['dateRangeBegin'], session['dateRangeEnd'],
                           session['startedAt'], session['endedAt'], session['reads'])

    def execute_session_command(self, session_id, session_version, session_command_type):
        ext = Routes.SYNC_SESSION_COMMAND % (session_id, session_command_type)
        url = self.base_url + ext
        body = {
            'id': session_id,
            'version': session_version
        }
        self.post_http_request(url, body)

    def fetch_sync_topic(self, session_id, topic, limit=1000, offset=0):
        params = {'limit': limit, 'offset': offset}
        url = f'{self.base_url}/{Routes.SYNC_SESSIONS}/{session_id}/{topic}'
        qr = self.get_http_request(url, params)
        return ListQueryResult(qr['results'], qr['offset'], qr['hasPreviousPage'], qr['hasNextPage'], qr['limit'],
                               qr['totalCount'], qr['empty'], qr['count'], qr['pageNumber'])

    def sync_filing_activities(self, session_id):
        limit, offset = 10, 0
        activities_qr = self.fetch_sync_topic(session_id, "activities", limit, offset)
        self.save_filing_activities(activities_qr.results)
        while activities_qr.hasNextPage:
            offset = offset + limit
            activities_qr = self.fetch_sync_topic(session_id, "activities", limit, offset)
            self.save_filing_activities(activities_qr.results)

    def save_filing_activities(self, filing_activities):
        for a in filing_activities:
            activity = FilingActivityV1(a['id'], a['version'], a['apiVersion'], a['creationDate'], a['lastUpdate'],
                                        a['activityType'], a['specificationKey'], a['origin'], a['filingId'],
                                        a['aid'], a['applyToFilingId'], a['publishSequence'])
            self.repository.save_filing_activity(activity)

    def sync_filing_activity_elements(self, session_id):
        limit, offset = 10, 0
        elements_qr = self.fetch_sync_topic(session_id, "activity-elements", limit, offset)
        self.save_filing_activity_elements(elements_qr.results)
        while elements_qr.hasNextPage:
            offset = offset + limit
            elements_qr = self.fetch_sync_topic(session_id, "activity-elements", limit, offset)
            self.save_filing_activity_elements(elements_qr.results)

    def save_filing_activity_elements(self, filing_elements):
        for e in filing_elements:
            element = FilingActivityElementV1(e['id'], e['apiVersion'], e['creationDate'], e['activityId'], e['activityType'],
                                              e['specificationKey'], e['origin'], e['originFilingId'],
                                              e['agencyId'], e['applyToFilingId'], e['publishSequence'],
                                              e['elementType'], e['elementIndex'], json.dumps(e['modelJson']))
            self.repository.save_filing_activity_element(element)

    def retrieve_sync_feed(self):
        url = self.base_url + Routes.SYNC_FEED
        feed = self.get_http_request(url)
        return SyncFeed(feed['id'], feed['version'], feed['productType'], feed['apiVersion'], feed['name'],
                        feed['description'], feed['status'], feed['topics'])

    def create_database_schema(self):
        self.repository.rebuild_schema()

    def post_http_request(self, url, body=None):
        response = requests.post(url, auth=(self.user, self.password), data=json.dumps(body), headers=self.headers)
        if response.status_code not in [200, 201]:
            raise Exception(f'Error requesting Url: {url}, Response code: {response.status_code}')
        return response.json()

    def get_http_request(self, url, params=None):
        response = requests.get(url, params=params, auth=(self.user, self.password), headers=self.headers)
        if response.status_code not in [200, 201]:
            raise Exception(f'Error requesting Url: {url}, Response code: {response.status_code}')
        return response.json()

    def main(self):
        try:
            # Build SQL DB
            self.create_database_schema()

            # Verify the system is ready
            sys_report = self.fetch_system_report()
            if sys_report.general_status == 'Ready':
                logging.info("Campaign API Sync is Ready")

                # Retrieve available SyncFeeds
                feed = self.retrieve_sync_feed()

                # Create SyncSubscription or use existing SyncSubscription with feed specified
                subscription = self.create_subscription(feed.id, "Feed_1")

                # Create SyncSession
                sync_session = self.create_session(subscription.id)

                # Synchronize Filing Activities
                self.sync_filing_activities(sync_session.id)

                # Synchronize Filing Elements
                self.sync_filing_activity_elements(sync_session.id)

                # Complete SyncSession
                self.execute_session_command(sync_session.id, sync_session.version,SyncSessionCommandType.Complete.name)

                # Cancel the subscription
                self.execute_subscription_command(subscription.id, subscription.version, SyncSubscriptionCommandType.Cancel.name)
            else:
                logging.info("The Campaign API system status is %s and is not Ready", sys_report.general_status)
        except Exception as ex:
            # Cancel Session on error
            if sync_session is not None:
                self.execute_session_command(sync_session.id, sync_session.version, SyncSessionCommandType.Cancel.name)
            logging.info("Error running CampaignApiClient: ", ex)


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
    api_user_arg = config[env]['API_USER']
    api_password_arg = config[env]['API_PASSWORD']
    db_host_arg = config[env]['HOST']
    db_name_arg = config[env]['DB_NAME']
    db_user_arg = config[env]['DB_USER']
    db_password_arg = config[env]['DB_PASSWORD']
    CampaignApiClient(api_url_arg, api_user_arg, api_password_arg, db_host_arg, db_name_arg, db_user_arg,
                      db_password_arg).main()

#!/usr/bin/python

import sys
import argparse
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
    SYNC_FEED = "/activity/v101/sync/feed"
    SYNC_SUBSCRIPTIONS = "/activity/v101/sync/subscriptions"
    SYNC_SESSIONS = "/activity/v101/sync/sessions"

    # First parameter is Session ID. Second parameter is Command Type
    SYNC_SESSION_COMMAND = "/activity/v101/sync/sessions/%s/commands/%s"

    # First parameter is Subscription ID. Second parameter is Command Type
    SYNC_SUBSCRIPTION_COMMAND = "/activity/v101/sync/subscriptions/%s/commands/%s"


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
        logging.debug('Checking to verify the Campaign API system is ready')
        url = self.base_url + Routes.SYSTEM_REPORT
        sr = self.get_http_request(url)
        system_report = SystemReport(sr['name'], sr['generalStatus'], sr['components'])
        logging.info('General Status: %s', system_report.general_status)
        logging.info('General Status: %s', system_report.name)
        for component in system_report.components:
            logging.info('\tComponent Name: %s', component.name)
            logging.info('\tComponent Message: %s', component.message)
            logging.info('\tComponent status: %s', component.status)
            logging.info('\tComponent Build DateTime: %s', component.build_date_time)
            logging.info('\tComponent Build Version: %s', component.build_version)
        return system_report

    def create_subscription(self, feed_name_arg, subscription_name_arg):
        logging.debug('Creating a SyncSubscription')
        url = self.base_url + Routes.SYNC_SUBSCRIPTIONS
        body = {
            'feedName': feed_name_arg,
            'name': subscription_name_arg
        }
        response = self.post_http_request(url, body)
        subscription = response['subscription']
        sync_sub = SyncSubscription(subscription['id'], subscription['version'], subscription['identityId'],
                                    subscription['feedId'], subscription['name'],subscription['autoComplete'],
                                    subscription['status'])
        self.repository.save_sync_subscription(sync_sub)
        logging.debug('SyncSubscription created successfully')
        return SyncSubscriptionResponse(response['executionId'], response['commandType'], response['subscription'], response['description'])

    def execute_subscription_command(self, sub_id, subscription_version, subscription_command_type):
        logging.debug(f'Executing {subscription_command_type} SyncSubscription command')
        ext = Routes.SYNC_SUBSCRIPTION_COMMAND % (sub_id, subscription_command_type)
        url = self.base_url + ext
        body = {
            'id': sub_id,
            'version': subscription_version
        }
        response = self.post_http_request(url, body)
        logging.debug(f'{subscription_command_type} SyncSubscription executed successfully')

        s = response['subscription']
        subscription = SyncSubscription(s['id'], s['version'], s['identityId'], s['feedId'], s['name'],
                                        s['autoComplete'], s['status'])
        self.repository.save_sync_subscription(subscription)
        return response

    def query_subscriptions(self, feed_id, limit=1000, offset=0):
        # TODO - Support paging of results
        logging.debug('Retrieving available subscriptions\n')
        params = {'feedId': feed_id, 'status': 'Active', 'limit': limit, 'offset': offset}
        url = self.base_url + Routes.SYNC_SUBSCRIPTIONS
        qr = self.get_http_request(url, params)
        return ListQueryResult(qr['results'], qr['offset'], qr['hasPreviousPage'], qr['hasNextPage'], qr['limit'],
                               qr['totalCount'], qr['empty'], qr['count'], qr['pageNumber'])

    def create_session(self, sub_id):
        logging.debug(f'Creating a SyncSession using SyncSubscription {sub_id}')
        url = self.base_url + Routes.SYNC_SESSIONS
        body = {
            'subscriptionId': sub_id
        }
        response = self.post_http_request(url, body)
        logging.debug(f'SyncSession using SyncSubscription {sub_id} created successfully')
        return SyncSessionResponse(response['executionId'], response['commandType'], response['session'],
                                   response['description'])

    def execute_session_command(self, session_id, session_version, session_command_type):
        logging.debug(f'Executing {session_command_type} SyncSession command')
        url = self.base_url + Routes.SYNC_SESSION_COMMAND % (session_id, session_command_type)
        body = {
            'version': session_version
        }
        response = self.post_http_request(url, body)
        logging.debug(f'{session_command_type} SyncSession executed successfully')
        return response

    def fetch_sync_topics(self, session_id, topic, limit=1000, offset=0):
        logging.debug(f'Fetching {topic} topic: offset={offset}, limit={limit}\n')
        params = {'limit': limit, 'offset': offset}
        url = f'{self.base_url}/{Routes.SYNC_SESSIONS}/{session_id}/{topic}'
        qr = self.get_http_request(url, params)
        return ListQueryResult(qr['results'], qr['offset'], qr['hasPreviousPage'], qr['hasNextPage'], qr['limit'],
                               qr['totalCount'], qr['empty'], qr['count'], qr['pageNumber'])

    def sync_filing_activities(self, session_id, limit):
        logging.debug('Syncing Filing Activities')
        offset = 0
        activities_qr = self.fetch_sync_topics(session_id, "activities", limit, offset)
        self.save_filing_activities(activities_qr.results)
        while activities_qr.hasNextPage:
            offset = offset + limit
            activities_qr = self.fetch_sync_topics(session_id, "activities", limit, offset)
            self.save_filing_activities(activities_qr.results)
        logging.debug('Filing Activities synchronized successfully')

    def save_filing_activities(self, filing_activities):
        for a in filing_activities:
            activity = FilingActivityV101(a['id'], a['version'], a['apiVersion'], a['creationDate'], a['lastUpdate'],
                                          a['activityType'], a['specificationKey'], a['origin'], a['filingId'],
                                          a['aid'], a['applyToFilingId'], a['publishSequence'])
            self.repository.save_filing_activity(activity)

    def sync_filing_activity_elements(self, session_id, limit):
        offset = 0
        elements_qr = self.fetch_sync_topics(session_id, "activity-elements", limit, offset)
        self.save_filing_activity_elements(elements_qr.results)
        while elements_qr.hasNextPage:
            offset = offset + limit
            elements_qr = self.fetch_sync_topics(session_id, "activity-elements", limit, offset)
            self.save_filing_activity_elements(elements_qr.results)

    def save_filing_activity_elements(self, filing_elements):
        for e in filing_elements:
            element = FilingActivityElementV101(e['id'], e['apiVersion'], e['creationDate'], e['activityId'], e['activityType'],
                                                e['specificationKey'], e['origin'], e['originFilingId'],
                                                e['agencyId'], e['applyToFilingId'], e['publishSequence'],
                                                e['elementType'], e['elementIndex'], json.dumps(e['modelJson']))
            self.repository.save_filing_activity_element(element)

    def retrieve_sync_feed(self):
        logging.debug('Retrieving SyncFeed')
        url = self.base_url + Routes.SYNC_FEED
        fd = self.get_http_request(url)
        return SyncFeed(fd['id'], fd['version'], fd['productType'], fd['apiVersion'], fd['name'],
                        fd['description'], fd['status'], fd['topics'])

    def create_database_schema(self):
        logging.debug('Creating database schema')
        self.repository.execute_sql_scripts()
        logging.debug('Database schema created successfully')

    def rebuild_database_schema(self):
        logging.debug('Rebuilding database schema')
        self.repository.rebuild_schema()

    def post_http_request(self, url, body=None):
        logging.debug(f'Making POST HTTP request to {url}')
        response = requests.post(url, auth=(self.user, self.password), data=json.dumps(body), headers=self.headers)
        if response.status_code not in [200, 201]:
            raise Exception(f'Error requesting Url: {url}, Response code: {response.status_code}. Error Message: {response.text}')
        return response.json()

    def get_http_request(self, url, params=None):
        logging.debug(f'Making GET HTTP request to {url}')
        response = requests.get(url, params=params, auth=(self.user, self.password), headers=self.headers)
        if response.status_code not in [200, 201]:
            raise Exception(f'Error requesting Url: {url}, Response code: {response.status_code}. Error Message: {response.text}')
        return response.json()


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

    campaign_api_client = CampaignApiClient(api_url_arg, api_user_arg, api_password_arg, db_host_arg, db_name_arg,
                                            db_user_arg, db_password_arg)

    parser = argparse.ArgumentParser(description='Process Campaign API Sync Requests')
    parser.add_argument('--re-sync', nargs=1, metavar='Subscription_Name', help='Find existing active subscription and sync available Feed Topics')
    parser.add_argument('--subscribe-and-sync', nargs=1, metavar='Subscription_Name',
                        help='create a new subscription and Sync available Feed Topics')
    parser.add_argument('--database', nargs=1, metavar='[create or rebuild]',
                        help='Create or Rebuild a local database schema')
    parser.add_argument('--create-subscription', nargs=2, metavar=('feed_name', 'subscription_name'),
                        help='create a new subscription')
    parser.add_argument('--cancel-subscription', nargs=2, metavar=('subscription_id', 'subscription_version'),
                        help='Cancel an existing subscription')
    parser.add_argument('--session', nargs=3, metavar=('[create, cancel, or complete]', 'session_id', 'session_version'),
                        help='create, cancel, or complete a session')
    parser.add_argument('--sync-topic', nargs=2, metavar=('session_id', 'topic_name'), help='sync a feed topic')
    parser.add_argument('--list-subscriptions', action='store_true', help='retrieve active subscriptions')
    parser.add_argument('--system-report', action='store_true', help='retrieve general system status')
    parser.add_argument('--feed', action='store_true', help='retrieve available feeds')
    # parser.add_argument('--version', action='version', help='Program Version Information')
    args = parser.parse_args()

    if args.re_sync:
        # Find existing active subscription for provided Subscription Name
        name = args.re_sync[0]
        subscriptions = campaign_api_client.repository.fetch_active_subscriptions_by_name(name)
        if len(subscriptions) == 0:
            print(f'No Active SyncSubscription found with Name {name}')
            sys.exit(1)
        # Create SyncSession
        sync_session_response = campaign_api_client.create_session(subscriptions[0].id)
        sess_id = sync_session_response.session.id
        version = sync_session_response.session.version

        # Synchronize Filing Activities
        page_size = 1000
        campaign_api_client.sync_filing_activities(sess_id, page_size)

        # Synchronize Filing Elements
        campaign_api_client.sync_filing_activity_elements(sess_id, page_size)

        # Complete SyncSession
        campaign_api_client.execute_session_command(sess_id, version, SyncSessionCommandType.Complete.name)
    elif args.subscribe_and_sync:
        # Retrieve available SyncFeeds
        feed = campaign_api_client.retrieve_sync_feed()

        # Create SyncSubscription or use existing SyncSubscription with feed specified
        subscription_name = args.subscribe_and_sync[0]
        subscription_response = campaign_api_client.create_subscription(feed.name, subscription_name)

        # Create SyncSession
        sync_session_response = campaign_api_client.create_session(subscription_response.subscription.id)
        sess_id = sync_session_response.session.id
        version = sync_session_response.session.version

        # Synchronize Filing Activities
        page_size = 1000
        campaign_api_client.sync_filing_activities(sess_id, page_size)

        # Synchronize Filing Elements
        campaign_api_client.sync_filing_activity_elements(sess_id, page_size)

        # Complete SyncSession
        campaign_api_client.execute_session_command(sess_id, version, SyncSessionCommandType.Complete.name)
    elif args.system_report:
        campaign_api_client.fetch_system_report()
    elif args.database:
        command = args.database[0]
        if command == 'create':
            campaign_api_client.repository.execute_sql_scripts()
        elif command == 'rebuild':
            campaign_api_client.repository.rebuild_schema()
    elif args.feed:
        sync_feed = campaign_api_client.retrieve_sync_feed()
        print(sync_feed)
    elif args.list_subscriptions:
        subs = campaign_api_client.repository.fetch_active_subscriptions()
        # Display subscription information
        output = f'Subscription Info:\n'
        for sub in subs:
            output += f'Subscription Name: {sub.name}, ID: {sub.id}, Version: {sub.version}\n'
        print(output)
    elif args.create_subscription:
        feed_name = args.create_subscription[0]
        subscription_name = args.create_subscription[1]
        sub_response = campaign_api_client.create_subscription(feed_name, subscription_name)
        print(sub_response)
    elif args.cancel_subscription:
        subscription_id = args.cancel_subscription[0]
        version = args.cancel_subscription[1]
        sub_response = campaign_api_client.execute_subscription_command(subscription_id, version, SyncSubscriptionCommandType.Cancel.name)
        print(sub_response)
    elif args.session:
        command = args.session[0]
        for arg in args.session:
            if command == 'create':
                subscription_id = args.session[1]
                session = campaign_api_client.create_session(subscription_id)
                print(session)
            elif command == 'cancel':
                sess_id = args.session[1]
                version = args.session[2]
                sub_response = campaign_api_client.execute_session_command(sess_id, version, SyncSessionCommandType.Cancel.name)
                print(sub_response)
            elif command == 'complete':
                sess_id = args.session[1]
                version = args.session[2]
                sub_response = campaign_api_client.execute_session_command(sess_id, version, SyncSessionCommandType.Complete.name)
                print(sub_response)
    elif args.sync_topic:
        sess_id = args.sync_topic[0]
        topic_name = args.sync_topic[1]
        page_size = 1000
        if topic_name == "activities":
            campaign_api_client.sync_filing_activities(sess_id, page_size)
        elif topic_name == "activity-elements":
            campaign_api_client.sync_filing_activity_elements(sess_id, page_size)

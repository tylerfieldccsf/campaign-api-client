#!/usr/bin/python

import argparse
import requests

from campaign_api_repository import *
from feed import SyncFeed
from session import *

import sys
sys.path.append('../')
from src import *

logger = logging.getLogger(__name__)


class Routes:
    SYSTEM_REPORT = '/system'
    SYNC_FEED = '/cal/v101/sync/feeds'
    SYNC_SUBSCRIPTIONS = '/cal/v101/sync/subscriptions'
    SYNC_SESSIONS = '/cal/v101/sync/sessions'

    # First parameter is Session ID. Second parameter is Command Type
    SYNC_SESSION_COMMAND = '/cal/v101/sync/sessions/%s/commands/%s'

    # First parameter is Subscription ID. Second parameter is Command Type
    SYNC_SUBSCRIPTION_COMMAND = '/cal/v101/sync/subscriptions/%s/commands/%s'

    # Parameter is the Subscription ID
    FETCH_SUBSCRIPTION = '/cal/v101/sync/subscriptions/%s'

    # First parameter is the Root Filing NID
    FETCH_FILING = '/cal/v101/filings/%s'
    FETCH_EFILE_CONTENT = '/cal/v101/filings/%s/contents/efiling'
    QUERY_FILINGS = '/cal/v101/filings'

    # First parameter is the Element ID
    FETCH_FILING_ELEMENTS = '/cal/v101/filing-elements/%s'
    QUERY_FILING_ELEMENTS = '/cal/v101/filing-elements'


class CampaignApiClient:
    """Provides support for synchronizing local database with Campaign API filing data"""
    def __init__(self, base_url, api_key, api_password, db_host, db_name, db_user, db_password):
        self.headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        self.base_url = base_url
        self.user = api_key
        self.password = api_password
        self.repository = CampaignApiRepository(db_host, db_name, db_user, db_password)

    def fetch_system_report(self):
        logger.debug('Checking to verify the Campaign API system is ready')
        url = self.base_url + Routes.SYSTEM_REPORT
        sr = self.get_http_request(url)
        system_report = SystemReport(sr['name'], sr['generalStatus'], sr['components'])
        logger.debug('General Status: %s', system_report.general_status)
        logger.debug('System Name: %s', system_report.name)
        for comp in system_report.components:
            logger.debug('\tComponent Name: %s', comp.name)
            logger.debug('\tComponent Message: %s', comp.message)
            logger.debug('\tComponent status: %s', comp.status)
            logger.debug('\tComponent Build DateTime: %s', comp.build_date_time)
            logger.debug('\tComponent Build Version: %s', comp.build_version)
        return system_report

    def create_subscription(self, feed_name_arg, subscription_name_arg):
        logger.debug('Creating a SyncSubscription')
        url = self.base_url + Routes.SYNC_SUBSCRIPTIONS
        body = {
            'feedName': feed_name_arg,
            'name': subscription_name_arg
        }
        response = self.post_http_request(url, body)
        subscription = response['subscription']
        sync_sub = SyncSubscription(subscription['id'], subscription['version'], subscription['identityId'],
                                    subscription['feedId'], subscription['name'], subscription['autoComplete'],
                                    subscription['status'])
        self.repository.save_sync_subscription(sync_sub)
        logger.debug('SyncSubscription created successfully')
        return SyncSubscriptionResponse(response['executionId'], response['commandType'], response['subscription'],
                                        response['description'])

    def fetch_subcription(self, sub_id):
        logger.debug(f"Fetching SyncSubscription with id: {sub_id}")
        ext = Routes.SYNC_SUBSCRIPTION_COMMAND % sub_id
        url = self.base_url + ext
        response = self.get_http_request(url)
        s = response['subscription']
        subscription = SyncSubscription(s['id'], s['version'], s['identityId'], s['feedId'], s['name'],
                                        s['autoComplete'], s['status'])
        self.repository.save_sync_subscription(subscription)
        return subscription

    def execute_subscription_command(self, sub_id, subscription_command_type):
        logger.debug(f"Executing {subscription_command_type} SyncSubscription command")
        ext = Routes.SYNC_SUBSCRIPTION_COMMAND % (sub_id, subscription_command_type)
        url = self.base_url + ext
        body = {
            'id': sub_id
        }
        response = self.post_http_request(url, body)
        logger.debug(f'{subscription_command_type} SyncSubscription executed successfully')

        s = response['subscription']
        subscription = SyncSubscription(s['id'], s['version'], s['identityId'], s['feedId'], s['name'],
                                        s['autoComplete'], s['status'])
        self.repository.save_sync_subscription(subscription)
        return SyncSubscriptionResponse(response['executionId'], response['commandType'], response['subscription'],
                                        response['description'])

    def query_subscriptions(self, feed_id, limit=1000, offset=0):
        # TODO - Support paging of results
        logger.debug('Retrieving available subscriptions\n')
        params = {'feedId': feed_id, 'status': 'Active', 'limit': limit, 'offset': offset}
        url = self.base_url + Routes.SYNC_SUBSCRIPTIONS
        qr = self.get_http_request(url, params)
        return ListQueryResult(qr['results'], qr['offset'], qr['hasPreviousPage'], qr['hasNextPage'], qr['limit'],
                               qr['totalCount'], qr['empty'], qr['count'], qr['pageNumber'])

    def create_session(self, sub_id):
        logger.debug(f'Creating a SyncSession using SyncSubscription {sub_id}')
        url = self.base_url + Routes.SYNC_SESSIONS
        body = {
            'subscriptionId': sub_id
        }
        response = self.post_http_request(url, body)
        logger.debug(f'SyncSession using SyncSubscription {sub_id} created successfully')
        return CreateSyncSessionResponse(response['syncDataAvailable'], response['session'], response['description'],
                                         response['topicLinks'])

    def execute_session_command(self, session_id, session_command_type):
        logger.debug(f'Executing {session_command_type} SyncSession command')
        url = self.base_url + Routes.SYNC_SESSION_COMMAND % (session_id, session_command_type)
        response = self.post_http_request(url)
        session_response = SyncSessionResponse(response['executionId'], response['commandType'], response['session'],
                                               response['description'])

        logger.debug(f'{session_command_type} SyncSession executed successfully')
        return session_response

    def fetch_sync_topics(self, session_id, topic, limit=1000, offset=0):
        logger.debug(f'Fetching {topic} topic: offset={offset}, limit={limit}\n')
        params = {'limit': limit, 'offset': offset}
        url = f'{self.base_url}/{Routes.SYNC_SESSIONS}/{session_id}/{topic}'
        qr = self.get_http_request(url, params)
        return ListQueryResult(qr['results'], qr['offset'], qr['hasPreviousPage'], qr['hasNextPage'], qr['limit'],
                               qr['totalCount'], qr['empty'], qr['count'], qr['pageNumber'])

    def sync_filing_activities(self, session_id, limit):
        logger.debug('Syncing Filing Activities')
        offset = 0
        activities_qr = self.fetch_sync_topics(session_id, 'filing-activities', limit, offset)
        self.save_filing_activities(activities_qr.results)
        while activities_qr.hasNextPage:
            offset = offset + limit
            activities_qr = self.fetch_sync_topics(session_id, 'filing-activities', limit, offset)
            self.save_filing_activities(activities_qr.results)
        logger.debug('Filing Activities synchronized successfully')

    def save_filing_activities(self, filing_activities):
        for a in filing_activities:
            activity = FilingActivityV101(a['filingActivityNid'], a['apiVersion'], a['creationDate'],
                                          a['lastUpdate'], a['activityType'], a['publishSequence'], a['filing'])
            self.repository.save_filing_activity(activity)

    def sync_element_activities(self, session_id, topic, limit):
        offset = 0
        elements_qr = self.fetch_sync_topics(session_id, topic, limit, offset)
        self.save_element_activities(elements_qr.results)
        while elements_qr.hasNextPage:
            offset = offset + limit
            elements_qr = self.fetch_sync_topics(session_id, topic, limit, offset)
            self.save_element_activities(elements_qr.results)

    def sync_transaction_activities(self, session_id, limit):
        offset = 0
        elements_qr = self.fetch_sync_topics(session_id, 'transaction-activities', limit, offset)
        self.save_element_activities(elements_qr.results)
        while elements_qr.hasNextPage:
            offset = offset + limit
            elements_qr = self.fetch_sync_topics(session_id, 'transaction-activities', limit, offset)
            self.save_element_activities(elements_qr.results)

    def save_element_activities(self, filing_elements):
        for e in filing_elements:
            element = ElementActivityV101(e['elementActivityNid'], e['apiVersion'], e['creationDate'],
                                          e['filingActivityNid'], e['activityType'], e['publishSequence'],
                                          e['element'])
            self.repository.save_element_activity(element)

    def retrieve_sync_feeds(self):
        logger.debug('Retrieving SyncFeed')
        url = self.base_url + Routes.SYNC_FEED
        feed_qr = self.get_http_request(url)
        fds = []
        for fd in feed_qr['results']:
            f = SyncFeed(fd['id'], fd['version'], fd['productType'], fd['apiVersion'], fd['name'],
                         fd['description'], fd['status'], fd['topics'])
            fds.append(f)
        return fds

    def fetch_filings(self, root_filing_nid):
        logger.debug(f'Fetching filing {root_filing_nid}')
        url = self.base_url + Routes.FETCH_FILING % root_filing_nid
        return self.get_http_request(url)

    def query_filings(self, query):
        logger.debug('Querying filings')
        url = self.base_url + Routes.QUERY_FILINGS
        params = {'Origin': query.origin, 'FilingId': query.filing_id, 'FilingSpecification': query.filing_specification,
                  'limit': query.limit, 'offset': query.offset}
        headers = {
            'Accept': 'application/json'
        }
        return self.get_http_request(url, params, headers)

    def fetch_filing_element(self, element_nid):
        logger.debug(f'Fetching filing {element_nid}')
        url = self.base_url + Routes.FETCH_FILING_ELEMENTS % element_nid
        return self.get_http_request(url)

    def query_filing_elements(self, query):
        logger.debug('Querying Filing Elements')
        url = self.base_url + Routes.QUERY_FILING_ELEMENTS
        params = {'Origin': query.origin, 'FilingId': query.filing_id,
                  'ElementClassification': query.element_classification, 'ElementType': query.element_type,
                  'limit': query.limit, 'offset': query.offset}
        headers = {
            'Accept': 'application/json'
        }
        return self.get_http_request(url, params, headers)

    def fetch_efile_content(self, root_filing_nid):
        logger.debug('Fetching Efile Content')
        url = self.base_url + Routes.FETCH_EFILE_CONTENT % root_filing_nid
        logger.debug(f'Making GET HTTP request to {url}')
        response = requests.get(url, params={'contentType': 'efile'}, auth=(self.user, self.password), headers=self.headers)
        if response.status_code not in [200, 201]:
            raise Exception(
                f'Error requesting Url: {url}, Response code: {response.status_code}. Error Message: {response.text}')
        file_content = response.text
        return file_content

    def create_database_schema(self):
        logger.debug('Creating database schema')
        self.repository.execute_sql_scripts()
        logger.debug('Database schema created successfully')

    def rebuild_database_schema(self):
        logger.debug('Rebuilding database schema')
        self.repository.rebuild_schema()

    def post_http_request(self, url, body=None):
        logger.debug(f'Making POST HTTP request to {url}')
        response = requests.post(url, auth=(self.user, self.password), data=json.dumps(body), headers=self.headers)
        if response.status_code not in [200, 201]:
            raise Exception(
                f'Error requesting Url: {url}, Response code: {response.status_code}. Error Message: {response.text}')
        return response.json()

    def get_http_request(self, url, params=None, headers=None):
        logger.debug(f'Making GET HTTP request to {url}')
        if headers is None:
            headers = self.headers
        response = requests.get(url, params=params, auth=(self.user, self.password), headers=headers)
        if response.status_code not in [200, 201]:
            raise Exception(
                f'Error requesting Url: {url}, Response code: {response.status_code}. Error Message: {response.text}')
        return response.json()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Campaign API Sync Requests')
    parser.add_argument('--re-sync', nargs=1, metavar='Subscription_Name',
                        help='Find existing active subscription and sync available Feed Topics')
    parser.add_argument('--subscribe-and-sync', nargs=1, metavar='Subscription_Name',
                        help='create a new subscription and Sync available Feed Topics')
    parser.add_argument('--database', nargs=1, metavar='[create or rebuild]',
                        help='Create or Rebuild a local database schema')
    parser.add_argument('--create-subscription', nargs=2, metavar=('feed_name', 'subscription_name'),
                        help='create a new subscription')
    parser.add_argument('--cancel-subscription', nargs=2, metavar=('subscription_id', 'subscription_version'),
                        help='Cancel an existing subscription')
    parser.add_argument('--session', nargs=3,
                        metavar=('[create, cancel, or complete]', 'session_id', 'session_version'),
                        help='create, cancel, or complete a session')
    parser.add_argument('--sync-topic', nargs=2, metavar=('session_id', 'topic_name'), help='sync a feed topic')
    parser.add_argument('--list-subscriptions', action='store_true', help='retrieve active subscriptions')
    parser.add_argument('--system-report', action='store_true', help='retrieve general system status')
    parser.add_argument('--feed', action='store_true', help='retrieve available feeds')

    args = parser.parse_args()

    if args.database:
        command = args.database[0]
        repository = CampaignApiRepository(db_host, db_name, db_user, db_password)
        if command == 'create':
            logger.info('Creating SQL schema')
            repository.execute_sql_scripts()
        elif command == 'rebuild':
            logger.info('Rebuilding SQL schema')
            repository.rebuild_schema()
        sys.exit()

    # First make sure that the Campaign API is ready
    campaign_api_client = CampaignApiClient(api_url, api_key, api_password, db_host, db_name, db_user, db_password)
    sys_report = campaign_api_client.fetch_system_report()
    try:
        if not sys_report.is_ready():
            logger.error('The Campaign API is not ready, current status is %s', sys_report.general_status)
            sys.exit()
        if args.re_sync:
            # Find existing active subscription for provided Subscription Name
            name = args.re_sync[0]
            logger.info('Re-syncing Filing Activities and Element Activities using subscription %s', name)
            subscriptions = campaign_api_client.repository.fetch_active_subscriptions_by_name(name)
            if len(subscriptions) == 0:
                logger.error(f'No Active SyncSubscription found with Name {name}')
                sys.exit()

            sync_session = None
            try:
                # Create SyncSession
                logger.info('Creating new session')
                sync_session_response = campaign_api_client.create_session(subscriptions[0].id)

                if sync_session_response.sync_data_available:
                    sync_session = sync_session_response.session
                    sess_id = sync_session.id

                    # Synchronize Filing Activities
                    logger.info('Synchronizing Filing Activities')
                    page_size = 1000
                    campaign_api_client.sync_filing_activities(sess_id, page_size)

                    # Synchronize Filing Elements
                    logger.info('Synchronizing Element Activities')
                    campaign_api_client.sync_element_activities(sess_id, 'element-activities', page_size)

                    # Synchronize Filing Elements
                    logger.info('Synchronizing Transaction Activities')
                    campaign_api_client.sync_element_activities(sess_id, 'transaction-activities', page_size)

                    # Complete SyncSession
                    logger.info('Completing session')
                    campaign_api_client.execute_session_command(sess_id, SyncSessionCommandType.Complete.name)
                else:
                    logger.info('No Sync Data Available')
                logger.info('Re-sync complete')
            except Exception as ex:
                # Cancel Session on error
                logger.error('Error attempting to re-sync with subscription %s: %s', subscriptions[0].name, ex)
                if sync_session is not None:
                    campaign_api_client.execute_session_command(sync_session.id, SyncSessionCommandType.Cancel.name)
                sys.exit()
        elif args.subscribe_and_sync:
            logger.info('Subscribe and sync Filing Activities and Element Activities')
            # Retrieve available SyncFeeds
            feeds = campaign_api_client.retrieve_sync_feeds()
            feed = feeds[0]
            logger.info('Sync Feed retrieved: %s', feed)

            # Create SyncSubscription or use existing SyncSubscription with feed specified
            subscription_name = args.subscribe_and_sync[0]
            sync_session = None
            try:
                logger.info('Creating new subscription with name %s', subscription_name)
                subscription_response = campaign_api_client.create_subscription(feed.name, subscription_name)
                subscription = subscription_response.subscription

                # Create SyncSession
                logger.info('Creating new session')
                sync_session_response = campaign_api_client.create_session(subscription.id)
                if sync_session_response.sync_data_available:
                    sync_session = sync_session_response.session
                    sess_id = sync_session.id

                    # Synchronize Filing Activities
                    logger.info('Synchronizing Filing Activities')
                    page_size = 1000
                    campaign_api_client.sync_filing_activities(sess_id, page_size)

                    # Synchronize Filing Elements
                    logger.info('Synchronizing Element Activities')
                    campaign_api_client.sync_element_activities(sess_id, page_size)

                    # Complete SyncSession
                    logger.info('Completing session')
                    campaign_api_client.execute_session_command(sess_id, SyncSessionCommandType.Complete.name)
                    logger.info('Sync complete')
                else:
                    logger.info('The Campaign API system status is %s and is not Ready', sys_report.general_status)
            except Exception as ex:
                # Cancel Session on error
                if sync_session is not None:
                    campaign_api_client.execute_session_command(sync_session.id, sync_session.version,
                                                                SyncSessionCommandType.Cancel.name)
                logger.error('Error attempting to subscribe and sync with subscription %s: %s', subscription.name, ex)
                sys.exit()
        elif args.system_report:
            logger.info('Fetching system report')
            report = campaign_api_client.fetch_system_report()
            logger.info('General Status: %s', report.general_status)
            logger.info('System Name: %s', report.name)
            for component in report.components:
                logger.info('\tComponent Name: %s', component.name)
                logger.info('\tComponent Message: %s', component.message)
                logger.info('\tComponent status: %s', component.status)
        elif args.feed:
            logger.info('Retrieving sync feed')
            sync_feeds = campaign_api_client.retrieve_sync_feeds()
            sync_feed = sync_feeds[0]
            logger.info('Sync Feed retrieved: %s', sync_feed)
        elif args.list_subscriptions:
            subs = campaign_api_client.repository.fetch_active_subscriptions()
            # Display subscription information
            output = f'Subscription Info:\n'
            for sub in subs:
                output += f'\t{sub}\n'
            logger.info(output)
        elif args.create_subscription:
            feed_name = args.create_subscription[0]
            subscription_name = args.create_subscription[1]
            logger.info('Creating new sync subscription with name %s', subscription_name)
            sub_response = campaign_api_client.create_subscription(feed_name, subscription_name)
            logger.info('New sync subscription created: %s', sub_response.subscription)
        elif args.cancel_subscription:
            subscription_id = args.cancel_subscription[0]
            version = args.cancel_subscription[1]
            sub_response = campaign_api_client.execute_subscription_command(subscription_id, SyncSubscriptionCommandType.Cancel.name)
            logger.info('Canceled subscription: %s', sub_response.subscription)
        elif args.session:
            command = args.session[0]
            if command == 'create':
                subscription_id = args.session[1]
                session_response = campaign_api_client.create_session(subscription_id)
                logger.info('New session created: %s', session_response.session)
            elif command == 'cancel':
                sess_id = args.session[1]
                version = args.session[2]
                sess_response = campaign_api_client.execute_session_command(sess_id, SyncSessionCommandType.Cancel.name)
                logger.info('Session canceled: %s', sess_response.session)
            elif command == 'complete':
                sess_id = args.session[1]
                version = args.session[2]
                try:
                    sess_response = campaign_api_client.execute_session_command(sess_id, SyncSessionCommandType.Complete.name)
                    logger.info('Sync Session complete: %s', sess_response.session)
                except Exception as ex:
                    logger.error('Error attempting to complete session with ID %s: %s', sess_id, ex)
        elif args.sync_topic:
            sess_id = args.sync_topic[0]
            topic_name = args.sync_topic[1]
            page_size = 1000
            if topic_name == 'filing-activities':
                logger.info('Synchronizing Filing Activities')
                campaign_api_client.sync_filing_activities(sess_id, page_size)
            elif topic_name == 'element-activities':
                logger.info('Synchronizing Element Activities')
                campaign_api_client.sync_element_activities(sess_id, 'element-activities', page_size)
            elif topic_name == 'transaction-activities':
                logger.info('Synchronizing Transaction Activities')
                campaign_api_client.sync_element_activities(sess_id, 'transaction-activities', page_size)
    finally:
        # Regardless of any issues during execution, close the database connection
        campaign_api_client.repository.close_connection()

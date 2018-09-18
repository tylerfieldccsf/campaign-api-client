#!/usr/bin/python

import sys
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
    # SYNC = "/activity/v101/sync"
    SYNC_FEED = "/activity/v101/sync/feed"
    SYNC_SUBSCRIPTIONS = "/activity/v101/sync/subscriptions"
    SYNC_SESSIONS = "/activity/v101/sync/sessions"

    # First parameter is Session ID. Second parameter is Command Type
    SYNC_SESSION_COMMAND = "/activity/v101/sync/sessions/%s/commands/%s"
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

    def create_subscription(self, feed_name, subscription_name):
        url = self.base_url + Routes.SYNC_SUBSCRIPTIONS
        body = {
            'feedName': feed_name,
            'name': subscription_name
        }
        sub_response = self.post_http_request(url, body)
        # sub = sub_response['subscription']
        # sync_sub = SyncSubscription(sub['id'], sub['version'], sub['identityId'], sub['feedId'], sub['name'],
        #                         sub['autoComplete'], sub['status'])
        #
        # self.repository.save_sync_subscription(sync_sub)
        return sub_response

    def execute_subscription_command(self, sub_id, subscription_version, subscription_command_type):
        ext = Routes.SYNC_SUBSCRIPTION_COMMAND % (sub_id, subscription_command_type)
        url = self.base_url + ext
        body = {
            'id': sub_id,
            'version': subscription_version
        }
        return self.post_http_request(url, body)

    def get_subscriptions(self, feed_id):
        # params = {'limit': limit, 'offset': offset}
        params = {'feedId': feed_id, 'status': 'Active'}
        url = self.base_url + Routes.SYNC_SUBSCRIPTIONS
        sub_response = self.get_http_request(url, params)
        sub = sub_response['subscription']
        sync_sub = SyncSubscription(sub['id'], sub['version'], sub['identityId'], sub['feedId'], sub['name'],
                                sub['autoComplete'], sub['status'])

        self.repository.save_sync_subscription(sync_sub)
        return sync_sub

    def create_session(self, sub_id):
        url = self.base_url + Routes.SYNC_SESSIONS
        body = {
            'subscriptionId': sub_id
        }
        session_response = self.post_http_request(url, body)
        # session = session_response['session']
        # return SyncSession(session['id'], session['version'], session['subscriptionId'], session['identityId'],
        #                    session['autoComplete'], session['status'], session['sequenceRangeBegin'],
        #                    session['sequenceRangeEnd'], session['dateRangeBegin'], session['dateRangeEnd'],
        #                    session['startedAt'], session['endedAt'], session['reads'])
        return session_response

    def execute_session_command(self, session_id, session_version, session_command_type):
        url = self.base_url + Routes.SYNC_SESSION_COMMAND % (session_id, session_command_type)
        body = {
            'version': session_version
        }
        return self.post_http_request(url, body)

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
        self.repository.execute_sql_scripts()

    def rebuild_database_schema(self):
        self.repository.rebuild_schema()

    def post_http_request(self, url, body=None):
        response = requests.post(url, auth=(self.user, self.password), data=json.dumps(body), headers=self.headers)
        if response.status_code not in [200, 201]:
            raise Exception(f'Error requesting Url: {url}, Response code: {response.status_code}. Error Message: {response.text}')
        return response.json()

    def get_http_request(self, url, params=None):
        response = requests.get(url, params=params, auth=(self.user, self.password), headers=self.headers)
        if response.status_code not in [200, 201]:
            raise Exception(f'Error requesting Url: {url}, Response code: {response.status_code}. Error Message: {response.text}')
        return response.json()

    def show_usage(self):
        print("Usage: blah blah")
        sys.exit(0)

    def execute_db_operations(self, command):
        if command == 'create':
            self.create_database_schema()
        elif command == 'rebuild':
            self.rebuild_database_schema()
        else:
            self.show_usage()

    def get_feed(self):
        return self.retrieve_sync_feed()

    def execute_list_subscriptions(self):
        return self.repository.fetch_active_subscriptions()

    def main(self):
        try:
            # Build SQL DB
            # self.rebuild_database_schema()

            sync_session = None

            # Verify the system is ready
            sys_report = self.fetch_system_report()
            if sys_report.general_status == 'Ready':
                logging.info("Campaign API Sync is Ready")

                # Retrieve available SyncFeeds
                feed = self.retrieve_sync_feed()

                # Create SyncSubscription or use existing SyncSubscription with feed specified
                subscription = self.create_subscription(feed.name, "My Campaign API Feed")

                # Get the current subscriptions
                # subscriptions = self.get_subscriptions(feed.id)

                # Create SyncSession
                sync_session = self.create_session(subscription.id)

                # Synchronize Filing Activities
                self.sync_filing_activities(sync_session.id)

                # Synchronize Filing Elements
                self.sync_filing_activity_elements(sync_session.id)

                # Complete SyncSession
                self.execute_session_command(sync_session.id, sync_session.version, SyncSessionCommandType.Complete.name)

                # Cancel the subscription
                resp = self.execute_subscription_command(subscription.id, subscription.version, SyncSubscriptionCommandType.Cancel.name)
                print(resp)
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
    logger.setLevel(logging.INFO)

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

    # CampaignApiClient(api_url_arg, api_user_arg, api_password_arg, db_host_arg, db_name_arg, db_user_arg,
    #                   db_password_arg).main()

    campaign_api_client = CampaignApiClient(api_url_arg, api_user_arg, api_password_arg, db_host_arg, db_name_arg, db_user_arg,
                                            db_password_arg)

    # Get Command line args
    args = sys.argv
    # logging.info(args)

    if len(args) < 2:
        campaign_api_client.show_usage()
        sys.exit(0)

    if args[1] == 'db':
        campaign_api_client.execute_db_operations(args[2])
    elif args[1] == 'feed':
        # User can retrieve feed information
        feed = campaign_api_client.get_feed()
        output = f'Feed Id: {feed.id}, Feed Name: {feed.name}, Topics: '
        for topic in feed.topics:
            output += f'Topic Name: {topic.name} Description: {topic.description}, '
        print(output)
    elif args[1] == 'subscription':
        # User can Create, Cancel, or List available subscriptions
        if(args[2]) == 'list':
            subs = campaign_api_client.execute_list_subscriptions()
            # Display subscription information
            output = f'Subscription Info:\n'
            for sub in subs:
                output += f'Subscription Name: {sub.name}, ID: {sub.id}, Version: {sub.version}\n'
            print(output)
        else:
            if args[2] == 'create':
                feed_name = args[3]
                subscription_name = args[4]
                response = campaign_api_client.create_subscription(feed_name, subscription_name)
                print(response)
            elif args[2] == 'cancel':
                subscription_id = args[2]
                version = args[3]
                response = campaign_api_client.execute_subscription_command(subscription_id, version, SyncSubscriptionCommandType.Cancel.name)
                print(response)
    elif args[1] == 'session':
        if args[2] == 'create':
            subscription_id = args[3]
            sync_session = campaign_api_client.create_session(subscription_id)
            print(sync_session)
        elif args[2] == 'cancel':
            session_id = args[3]
            version = args[4]
            response = campaign_api_client.execute_session_command(session_id, version, SyncSessionCommandType.Cancel.name)
            print(response)
        elif args[2] == 'complete':
            session_id = args[3]
            version = args[4]
            response = campaign_api_client.execute_session_command(session_id, version, SyncSessionCommandType.Complete.name)
            print(response)
    elif args[1] == 'topic':
        session_id = args[2]
        topic_name = args[3]
        if topic_name == "activities":
            campaign_api_client.sync_filing_activities(session_id)
        elif topic_name == "activity-elements":
            campaign_api_client.sync_filing_activity_elements(session_id)
    else:
        campaign_api_client.show_usage()

    sys.exit(0)

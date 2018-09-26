import sys
import logging
from subscription import *
from session import *
import json
from campaign_api_client import CampaignApiClient


def main(api_url, api_user, api_password, db_host, db_name, db_user, db_password):
    """
    This demonstrates the complete lifecycle of the Campaign API sync process.
    1) Create a SyncSubscription
    2) Create a SyncSession using the SyncSubscription. This will be the start of the session
    3) Synchronize FilingActivities
    4) Synchronize ElementActivities
    5) Complete the SyncSession. This will be the end of the session
    6) Cancel the SyncSubscription. SyncSubscriptions are long living, and do not need to be canceled between SyncSessions

    :param api_url: Base URL of the API. Example - "https://netfile.com/filing/api"
    :param api_user: Username credential to authenticate against the Campaign API
    :param api_password: Password credential to authenticate against the Campaign API
    :param db_host: Name of host to connect to PostgreSQL database
    :param db_name: Postgres database to connect to
    :param db_user: Postgres database username
    :param db_password: Postgres database password
    """
    sync_session = None
    api_client = None
    try:
        logging.info("Starting Campaign API synchronization lifecycle")
        api_client = CampaignApiClient(api_url, api_user, api_password, db_host, db_name, db_user, db_password)

        # Re-Build SQL DB. This will drop all existing tables and data and re-create the schema
        logging.info("Rebuilding database schema")
        api_client.rebuild_database_schema()

        # Verify the system is ready
        sys_report = api_client.fetch_system_report()
        if sys_report.is_ready():
            logging.info("Campaign API Sync is Ready")

            # Retrieve available SyncFeeds
            logging.info("Retrieving available sync feed")
            feed = api_client.retrieve_sync_feed()

            # Create SyncSubscription or use existing SyncSubscription with feed specified
            name = "My Campaign API Feed"
            logging.info("Creating new subscription with name '%s'", name)
            subscription_response = api_client.create_subscription(feed.name, name)

            # Create SyncSession
            logging.info("Creating sync session")
            subscription = subscription_response.subscription
            sync_session_response = api_client.create_session(subscription.id)

            # Synchronize Filing Activities
            logging.info("Synchronizing Filing Activities")
            sync_session = sync_session_response.session
            page_size = 10
            api_client.sync_filing_activities(sync_session.id, page_size)

            # Synchronize Filing Elements
            logging.info("Synchronizing Element Activities")
            api_client.sync_element_activities(sync_session.id, page_size)

            # Complete SyncSession
            logging.info("Completing sync session")
            api_client.execute_session_command(sync_session.id, sync_session.version, SyncSessionCommandType.Complete.name)

            # Cancel the subscription
            logging.info("Canceling subscription")
            api_client.execute_subscription_command(subscription.id, subscription.version, SyncSubscriptionCommandType.Cancel.name)

            logging.info("Synchronization lifecycle complete")
        else:
            logging.info("The Campaign API system status is %s and is not Ready", sys_report.general_status)
    except Exception as ex:
        # Cancel Session on error
        if sync_session is not None:
            logging.info("Error occurred, canceling sync session")
            api_client.execute_session_command(sync_session.id, sync_session.version, SyncSessionCommandType.Cancel.name)
        logging.error('Error running CampaignApiClient: %s', ex)
        sys.exit()
    finally:
        api_client.repository.conn.close()


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

    env = "TEST"
    api_url_arg = config[env]['API_URL']
    api_user_arg = config[env]['API_USER']
    api_password_arg = config[env]['API_PASSWORD']
    db_host_arg = config[env]['HOST']
    db_name_arg = config[env]['DB_NAME']
    db_user_arg = config[env]['DB_USER']
    db_password_arg = config[env]['DB_PASSWORD']

    main(api_url_arg, api_user_arg, api_password_arg, db_host_arg, db_name_arg, db_user_arg, db_password_arg)

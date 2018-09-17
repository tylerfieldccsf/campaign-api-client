import unittest
import json
import logging
from campaign_api_repository import CampaignApiRepository
from tests.data_factory import *


class TestCampaignApiRepository(unittest.TestCase):

    def setUp(self):
        with open('../resources/config.json', 'r') as f:
            config = json.load(f)

        db_host = config['TEST']['HOST']
        db_name = config['TEST']['DB_NAME']
        db_user = config['TEST']['DB_USER']
        db_password = config['TEST']['DB_PASSWORD']
        self.repository = CampaignApiRepository(db_host, db_name, db_user, db_password)
        self.assertIsNotNone(self.repository)

    def test01_rebuild_db(self):
        """Rebuild campaign-api-sync database schema. This will drop existing tables during rebuild."""
        self.repository.rebuild_schema()

    def test02_filing_activity(self):
        logging.info("Running Filing Activity Test...")
        # Persist a FilingActivity
        self.repository.save_filing_activity(filing_activity)

        # fetch FilingActivity and assert stuff
        activity = self.repository.fetch_filing_activity(filing_activity.id)
        self.assertIsNotNone(activity)
        self.assertEquals("New", activity.activity_type)
        self.assertEquals("I come from the land down under", activity.origin)
        self.assertEquals("filing_101", activity.filing_id)

        # delete the FilingActivity
        # self.repository.delete_filing_activity(filing_activity.id)
        # activity = self.repository.fetch_filing_activity(filing_activity.id)
        # self.assertIsNone(activity)

    def test03_filing_activity_element(self):
        logging.info("Running Filing Element Test...")
        # Persist a FilingActivity
        self.repository.save_filing_activity_element(filing_activity_element)

        # fetch FilingActivity and assert stuff
        element = self.repository.fetch_filing_activity_element(filing_activity_element.id)
        self.assertIsNotNone(element)
        self.assertEquals("New", element.activity_type)
        self.assertEquals("I come from the land down under", element.origin)
        self.assertEquals("filing_101", element.origin_filing_id)

    def test04_sync_subscription(self):
        logging.info("Testing Sync Subscription")
        # Save subscription
        self.repository.save_sync_subscription(active_sync_subscription)

        # Retrieve sub by ID
        sub = self.repository.fetch_subscription(active_sync_subscription.id)
        self.assertIsNotNone(sub)
        self.assertEquals("Test Feed", sub.name)
        self.assertEquals("active", sub.status)
        self.assertEquals(0, sub.version)
        self.assertEquals(active_sync_subscription.id, sub.id)
        self.assertEquals(active_sync_subscription.identity_id, sub.identity_id)
        self.assertEquals(active_sync_subscription.feed_id, sub.feed_id)
        self.assertEquals(False, sub.auto_complete)

        # Retrieve sub by fetchActiveSubs
        is_found = False
        subs = self.repository.fetch_active_subscriptions()
        for s in subs:
            if s.id == active_sync_subscription.id:
                is_found = True
        self.assertTrue(is_found)

        # Cancel subscription
        self.repository.cancel_subscription(active_sync_subscription.id)
        sub = self.repository.fetch_subscription(active_sync_subscription.id)
        self.assertIsNotNone(sub)
        self.assertEquals("canceled", sub.status)

        # Delete the subscription
        self.repository.delete_subscription(active_sync_subscription.id)
        sub = self.repository.fetch_subscription(active_sync_subscription.id)
        self.assertIsNone(sub)


if __name__ == '__main__':
    unittest.main()

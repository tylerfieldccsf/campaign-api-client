import unittest
from campaign_api_repository import CampaignApiRepository

import sys
sys.path.append('../')

from tests.data_factory import *
from src import *

logger = logging.getLogger(__name__)


class TestCampaignApiRepository(unittest.TestCase):

    def setUp(self):
        self.repository = CampaignApiRepository(db_host_unit_test, db_name_unit_test, db_user_unit_test, db_password_unit_test)
        self.assertIsNotNone(self.repository)

    def tearDown(self):
        self.repository.close_connection()

    def test01_rebuild_db(self):
        """Rebuild campaign-api-sync database schema. This will drop existing tables during rebuild."""
        self.repository.rebuild_schema()

    def test02_filing_activity(self):
        logging.info('Running Filing Activity Test...')
        # Persist a FilingActivity
        self.repository.save_filing_activity(filing_activity)

        # fetch FilingActivity and assert stuff
        activity = self.repository.fetch_filing_activity(filing_activity.filing_activity_nid)
        self.assertIsNotNone(activity)
        self.assertEqual('New', activity.activity_type)
        self.assertEqual('I come from the land down under', activity.filing.filing_meta.legal_origin)

    def test03_filing_activity_element(self):
        logging.info('Running Element Activity Test...')
        # Persist a FilingActivity
        self.repository.save_element_activity(element_activity)

        # fetch FilingActivity and assert stuff
        element = self.repository.fetch_element_activity(element_activity.element_activity_nid)
        self.assertIsNotNone(element)
        self.assertEqual('New', element.activity_type)

    def test04_sync_subscription(self):
        logging.info('Testing Sync Subscription')
        # Save subscription
        self.repository.save_sync_subscription(active_sync_subscription)

        # Retrieve sub by ID
        sub = self.repository.fetch_subscription(active_sync_subscription.id)
        self.assertIsNotNone(sub)
        self.assertEqual('Test Feed', sub.name)
        self.assertEqual('Active', sub.status)
        self.assertEqual(0, sub.version)
        self.assertEqual(active_sync_subscription.id, sub.id)
        self.assertEqual(active_sync_subscription.identity_id, sub.identity_id)
        self.assertEqual(active_sync_subscription.feed_id, sub.feed_id)
        self.assertEqual(False, sub.auto_complete)

        # Retrieve sub by name
        subs = self.repository.fetch_active_subscriptions_by_name('Test Feed')
        self.assertIsNotNone(subs)
        self.assertTrue(len(subs) > 0)
        self.assertEqual('Test Feed', subs[0].name)
        self.assertEqual('Active', subs[0].status)

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
        self.assertEqual('canceled', sub.status)

        # Delete the subscription
        self.repository.delete_subscription(active_sync_subscription.id)
        sub = self.repository.fetch_subscription(active_sync_subscription.id)
        self.assertIsNone(sub)


if __name__ == '__main__':
    unittest.main()

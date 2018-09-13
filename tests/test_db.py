import unittest
import json
import logging
from db_util import PostgresDbUtil
from tests.data_factory import *


class TestDB(unittest.TestCase):

    def setUp(self):
        with open('../resources/config.json', 'r') as f:
            config = json.load(f)

        db_host = config['TEST']['HOST']
        db_name = config['TEST']['DB_NAME']
        db_user = config['TEST']['DB_USER']
        db_password = config['TEST']['DB_PASSWORD']
        self.postgres_util = PostgresDbUtil(db_host, db_name, db_user, db_password)
        self.assertIsNotNone(self.postgres_util)

    def test_rebuild_db(self):
        """Rebuild campaign-api-sync database schema. This will drop existing tables during rebuild."""
        self.postgres_util.rebuild_schema()

    def test_filing_activity(self):
        logging.info("Running Filing Activity Test...")
        # Persist a FilingActivity
        self.postgres_util.save_filing_activity(filing_activity)

        # fetch FilingActivity and assert stuff
        activity = self.postgres_util.fetch_filing_activity(filing_activity.id)
        self.assertIsNotNone(activity)
        self.assertEquals("New", activity.filing_activity_type)
        self.assertEquals("I come from the land down under", activity.origin)
        self.assertEquals("filing_101", activity.origin_filing_id)

        # delete the FilingActivity
        self.postgres_util.delete_filing_activity(filing_activity.id)
        activity = self.postgres_util.fetch_filing_activity(filing_activity.id)
        self.assertIsNone(activity)

    def test_filing_element(self):
        logging.info("Running Filing Element Test...")
        # Persist a FilingActivity
        self.postgres_util.save_filing_element(filing_element)

        # fetch FilingActivity and assert stuff
        element = self.postgres_util.fetch_filing_element(filing_element.id)
        self.assertIsNotNone(element)
        self.assertEquals("New", element.filing_activity_type)
        self.assertEquals("I come from the land down under", element.origin)
        self.assertEquals("filing_101", element.origin_filing_id)

        # delete the FilingActivity
        self.postgres_util.delete_filing_element(filing_element.id)
        element = self.postgres_util.fetch_filing_element(filing_element.id)
        self.assertIsNone(element)


if __name__ == '__main__':
    unittest.main()

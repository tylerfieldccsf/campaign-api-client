import unittest
import json
from db.db_util import PostgresDbUtil
from tests.data_factory import *


class TestCreateDB(unittest.TestCase):

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

    def test_flare_activity(self):
        # Persist a FlareActivity
        self.postgres_util.save_flare_activity(flare_activity)

        # fetch FlareActivity and assert stuff
        activity = self.postgres_util.fetch_flare_activity(flare_activity.id)
        self.assertIsNotNone(activity)
        self.assertEquals("New", activity.filing_activity_type)
        self.assertEquals("I come from the land down under", activity.origin)
        self.assertEquals("filing_101", activity.origin_filing_id)

        # delete the FlareActivity
        self.postgres_util.delete_flare_activity(flare_activity.id)
        activity = self.postgres_util.fetch_flare_activity(flare_activity.id)
        self.assertIsNone(activity)

    def test_flare_element(self):
        # Persist a FlareActivity
        self.postgres_util.save_flare_element(flare_element)

        # fetch FlareActivity and assert stuff
        element = self.postgres_util.fetch_flare_element(flare_element.id)
        self.assertIsNotNone(element)
        self.assertEquals("New", element.filing_activity_type)
        self.assertEquals("I come from the land down under", element.origin)
        self.assertEquals("filing_101", element.origin_filing_id)

        # delete the FlareActivity
        self.postgres_util.delete_flare_element(flare_element.id)
        element = self.postgres_util.fetch_flare_element(flare_element.id)
        self.assertIsNone(element)


if __name__ == '__main__':
    unittest.main()

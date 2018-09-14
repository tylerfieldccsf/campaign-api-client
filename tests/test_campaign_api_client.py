import unittest
import campaign_api_client
import json
import logging
from campaign_api_client import CampaignApiClient


class TestCampaignApiClient(unittest.TestCase):

    def setUp(self):
        with open('../resources/config.json', 'r') as f:
            config = json.load(f)

        env = "TEST"
        api_url = config[env]['API_URL']
        api_user = config[env]['API_USER']
        api_password = config[env]['API_PASSWORD']
        db_host = config[env]['HOST']
        db_name = config[env]['DB_NAME']
        db_user = config[env]['DB_USER']
        db_password = config[env]['DB_PASSWORD']
        self.api_client = CampaignApiClient(api_url, api_user, api_password, db_host, db_name, db_user, db_password)

    def test02_system_report(self):
        logging.info("Running System Report Test...")
        system_report = self.api_client.fetch_system_report()
        self.assertIsNotNone(system_report)
        self.assertEqual('Ready', system_report.general_status)
        self.assertEqual('FilingExt', system_report.name)
        self.assertTrue(system_report.components.__len__() > 0)
        logging.info("System Report Test Complete...")


if __name__ == '__main__':
    unittest.main()

import unittest
import campaign_api_client
import json
import logging
from campaign_api_client import CampaignApiClient


class TestCampaignApiClient(unittest.TestCase):

    def setUp(self):
        with open('../resources/config.json', 'r') as f:
            config = json.load(f)

        api_url = config['TEST']['API_URL']
        db_host = config['TEST']['HOST']
        db_name = config['TEST']['DB_NAME']
        db_user = config['TEST']['DB_USER']
        db_password = config['TEST']['DB_PASSWORD']
        self.api_client = CampaignApiClient(api_url, db_host, db_name, db_user, db_password)

    def test01(self):
        campaign_api_client.sync_filings()

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

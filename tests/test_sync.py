import unittest
import campaign_api_client
import json
from campaign_api_http_client import CampaignApiHttpClient


class TestSync(unittest.TestCase):

    def setUp(self):
        with open('../resources/config.json', 'r') as f:
            config = json.load(f)

        db_host = config['TEST']['API_URL']
        self.http_client = CampaignApiHttpClient(db_host)

    def test1(self):
        campaign_api_client.say_hello()

    def test_system_report(self):
        system_report = self.http_client.fetch_system_report()
        self.assertIsNotNone(system_report)
        self.assertEqual('Ready', system_report.general_status)
        self.assertEqual('FilingCapsule', system_report.name)
        self.assertTrue(system_report.components.__len__() > 0)


if __name__ == '__main__':
    unittest.main()

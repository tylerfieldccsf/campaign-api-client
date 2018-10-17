import unittest

from src import *
from campaign_api_http_client import CampaignApiHttpClient


class TestCampaignApiHttpClient(unittest.TestCase):

    def setUp(self):
        self.api_client = CampaignApiHttpClient(api_url, api_user, api_password, db_host, db_name, db_user, db_password)

    def test02_system_report(self):
        logging.info('Running System Report Test...')
        system_report = self.api_client.fetch_system_report()
        self.assertIsNotNone(system_report)
        self.assertEqual('Ready', system_report.general_status)
        self.assertEqual('FilingExt', system_report.name)
        self.assertTrue(system_report.components.__len__() > 0)
        logging.info('System Report Test Complete...')

    def test03_search_filing(self):
        # Query for filing
        # query = FilingQuery('NetFileAdmin', None, 'CAL:Fppc460:2.01')
        query = FilingQuery()
        response = self.api_client.query_filings(query)
        self.assertIsNotNone(response)

        # Fetch a filing by ID
        root_filing_nid = '79935105-da2d-4934-b363-bab537076c68'
        response = self.api_client.fetch_filings(root_filing_nid)
        print(response)

    def test04_search_element(self):
        # Query for filing element
        query = FilingElementQuery()
        response = self.api_client.query_filing_elements(query)
        self.assertIsNotNone(response)

    def test05_fetch_efile_content(self):
        pass


if __name__ == '__main__':
    unittest.main()

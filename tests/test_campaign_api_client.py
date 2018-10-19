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
        # Query filings using no criteria
        query = FilingQuery()
        response = self.api_client.query_filings(query)
        self.assertIsNotNone(response)
        results = response['results']
        self.assertTrue(len(results) > 0)

        # Create Filings for the results
        filings = []
        for result in results:
            filingV101 = FilingV101(result['filingNid'], result['rootFilingNid'], result['filingMeta'], result['filerMeta'], result['agencyMeta'])
            filings.append(filingV101)

        # Fetch a filing by ID
        filing = filings[0]
        root_filing_nid = filing.root_filing_nid
        response = self.api_client.fetch_filings(root_filing_nid)
        fetched_filing = FilingV101(response['filingNid'], response['rootFilingNid'], response['filingMeta'],
                                    response['filerMeta'], response['agencyMeta'])

        # TODO - Compare more properties to verify we have the right Filing
        self.assertEqual(filing.root_filing_nid, fetched_filing.root_filing_nid)

    def test04_search_element(self):
        # Query for filing elements using no criteria
        query = FilingElementQuery()
        response = self.api_client.query_filing_elements(query)
        self.assertIsNotNone(response)
        list_qr = ListQueryResult(response['results'], response['offset'], response['hasPreviousPage'],
                                  response['hasNextPage'], response['limit'], response['totalCount'],
                                  response['empty'], response['count'], response['pageNumber'])
        elements = []
        for e in list_qr.results:
            elementV101 = FilingElementV101(e['elementNid'], e['rootElementNid'], e['filingNid'], e['rootFilingNid'],
                                            e['specificationKey'], e['elementClassification'], e['elementType'],
                                            e['elementIndex'], e['elementModel'])
            elements.append(elementV101)

        element = elements[0]
        element_nid = element.element_nid
        response = self.api_client.fetch_filing_element(element_nid)
        fetched_element = FilingElementV101(response['elementNid'], response['rootElementNid'], response['filingNid'],
                                            response['rootFilingNid'], response['specificationKey'],
                                            response['elementClassification'], response['elementType'],
                                            response['elementIndex'], response['elementModel'])

        # TODO - Compare more properties to verify we have the right Filing Element
        self.assertEqual(element.element_nid, fetched_element.element_nid)

    def test05_fetch_efile_content(self):
        # Query filings using no criteria
        query = FilingQuery()
        response = self.api_client.query_filings(query)
        self.assertIsNotNone(response)
        results = response['results']
        self.assertTrue(len(results) > 0)

        # Create Filings for the results
        filings = []
        for result in results:
            filingV101 = FilingV101(result['filingNid'], result['rootFilingNid'], result['filingMeta'],
                                    result['filerMeta'], result['agencyMeta'])
            filings.append(filingV101)

        # Fetch a filing by ID
        filing = filings[0]
        root_filing_nid = filing.root_filing_nid

        # Fetch the efile content for this filing
        file_content = self.api_client.fetch_efile_content(root_filing_nid)

        # Verify efile contents
        self.assertTrue('HDR,CAL' in file_content)


if __name__ == '__main__':
    unittest.main()

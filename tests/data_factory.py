import uuid
from datetime import datetime
from topics import *
from subscription import *

# Assign variables for FilingActivity and FilingElement
filing_activity_nid = str(uuid.uuid4())
version = 0
api_version = "V101"
creation_date = datetime.now()
last_update = datetime.now()
activity_type = "New"
activity_status = "Created"
specification_key = "filing:specification:key"
legal_origin = "I come from the land down under"
filing_id = "filing_101"
aid = "AHW"
apply_to_legal_filing_id = "SFO-12345"
publish_sequence = 25
filing_nid = str(uuid.uuid4())
form_id = str(uuid.uuid4())
root_filing_nid = str(uuid.uuid4())
legal_filing_id = "11111"
legal_filing_date = datetime.now()
start_date = datetime.now()
end_date = datetime.now()
report_number = 1
client_dataspace_id = str(uuid.uuid4())
application_dataspace_id = str(uuid.uuid4())

address = "4E3FF207CBE1820E09BF8D061ACECF76C368D009FFEE929DCFECDA7FEF8348A8124586AC1148D9C0F99C9E91C09CC905E58AE01A5C23E6186914F07718ABF404"

filing_meta = {'legalOrigin': legal_origin, 'legalFilingId': legal_filing_id, 'specificationKey': specification_key,
               'formId': form_id, 'legalFilingDate': legal_filing_date, 'startDate': start_date, 'endDate': end_date,
               'reportNumber': report_number, 'applyToLegalFilingId': apply_to_legal_filing_id}
filer_meta = {'longId': 12345, 'stringId': '12345', 'commonName': 'John Doe', 'systemizedName': 'CA_123',
              'status': "active", 'phoneList': '(559)111-0222,(559)111-0223',
              'emailList': 'john@example.com,doe@example.com', 'addressList': '123 A Street'}
agency_meta = {'aid': aid, 'clientDataspaceId': client_dataspace_id, 'applicationDataspaceId': application_dataspace_id}

filing = {'filingNid': filing_nid, 'apiVersion': api_version, 'rootFilingNid': root_filing_nid,
          'filingMeta': filing_meta, 'filerMeta': filer_meta, 'agencyMeta': agency_meta}
filing_activity = FilingActivityV101(filing_activity_nid, api_version, creation_date, last_update, activity_type,
                                     publish_sequence, filing)

element_type = "test:element:specification"
element_index = '0'
element_classification = "header"
element_nid = str(uuid.uuid4())
root_element_nid = str(uuid.uuid4())
json_body = """{"date": "2015-10-11T00:00:00", "amount": 500.00, "isMemo": false, "splits": [], 
"dateTwo": "0001-01-01T00:00:00", "formType": "A", "treasurer": {"prefix": "", "suffix": "", "isEmpty": true, 
"fullName": "", "lastName": "", "firstName": "", "fullNameWithPrefixAndSuffix": ""}, "entityCode": "Individual", 
"fieldCount": 66, "recordType": "RCPT", "contributor": {"prefix": "", "suffix": "", "isEmpty": false, 
"fullName": "Smith, John", "lastName": "Smith", "firstName": "John", "fullNameWithPrefixAndSuffix": "John Smith"}, 
"description": "", "publicNotes": [], "intermediary": {"prefix": "", "suffix": "", "isEmpty": true, "fullName": "", 
"lastName": "", "firstName": "", "fullNameWithPrefixAndSuffix": ""}, "cumulativeYTD": 150.00, "memoReference": "", 
"transactionId": "INC57", "backReferenceId": "", "transactionType": "Unset", "treasurerAddress": {"zip": "", "city": "",
 "line1": "", "line2": "", "state": "", "isEmpty": true, "cityStateZip": "", "streetAddress": ""}, 
 "contributorAddress": {"zip": "94612", "city": "Oakland", "line1": "560 Thomas L. Berkley Way", "line2": "", 
 "state": "CA", "isEmpty": false, "cityStateZip": "Oakland, CA 94612", "streetAddress": "560 Thomas L. Berkley Way"}, 
 "contributorEmployer": "The Big Union", "intermediaryAddress": {"zip": "", "city": "", "line1": "", "line2": "", 
 "state": "", "isEmpty": true, "cityStateZip": "", "streetAddress": ""}, "intermediaryEmployer": "", 
 "contributorOccupation": "Chief", "contributorCommitteeId": "", "intermediaryOccupation": "", 
 "intermediaryCommitteeId": "", "contributorIsSelfEmployed": false, "intermediaryIsSelfEmployed": false}"""
element = {'apiVersion': api_version, 'elementNid': element_nid, 'rootElementNid': root_element_nid,
           'filingNid': filing_nid, 'rootFilingNid': root_filing_nid, 'specificationKey': specification_key,
           'elementClassification': element_classification, 'elementType': element_type,
           'elementIndex': element_index, 'elementModel': json_body}

element_activity = ElementActivityV101(api_version, str(uuid.uuid4()), creation_date, activity_type,
                                       activity_status, publish_sequence, element)

identity_id = str(uuid.uuid4())
feed_id = str(uuid.uuid4())
active_sync_subscription = SyncSubscription(str(uuid.uuid4()), version, identity_id, feed_id, "Test Feed", False, "Active")
canceled_sync_subscription = SyncSubscription(str(uuid.uuid4()), 1, identity_id, feed_id, "Test Feed", False, "canceled")

import uuid
from datetime import datetime
from models import *

# Assign variables for FilingActivity and FilingElement
id_arg = uuid.uuid4()
version = 0
creation_date = datetime.now()
last_update = datetime.now()
filing_activity_type = FilingActivityType.New.name
filing_specification_key = "filing:specification:key"
origin = "I come from the land down under"
origin_filing_id = "filing_101"
agency_id = "AHW"
apply_to_filing_id = None
publish_sequence = 25

address = "4E3FF207CBE1820E09BF8D061ACECF76C368D009FFEE929DCFECDA7FEF8348A8124586AC1148D9C0F99C9E91C09CC905E58AE01A5C23E6186914F07718ABF404 "
filing_activity = FilingActivityV1(str(id_arg), version, creation_date, last_update, filing_activity_type, filing_specification_key,
                                   origin, origin_filing_id, agency_id, apply_to_filing_id, publish_sequence)

element_specification = "test:element:specification"
element_index = 0
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
filing_element = FilingElementV1(str(uuid.uuid4()), creation_date, str(id_arg), filing_activity_type, filing_specification_key,
                                 origin, origin_filing_id, agency_id, apply_to_filing_id, publish_sequence,
                                 element_specification, element_index, json_body)

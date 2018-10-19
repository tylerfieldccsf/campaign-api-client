import uuid
from datetime import datetime
from filing import *
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

filing = {'filingNid': filing_nid, 'rootFilingNid': root_filing_nid, 'filingMeta': filing_meta,
          'filerMeta': filer_meta, 'agencyMeta': agency_meta}
filing_activity = FilingActivityV101(filing_activity_nid, api_version, creation_date, last_update, activity_type,
                                     publish_sequence, filing)

element_type = "ScheduleB12"
element_index = '0'
element_classification = "transaction"
element_nid = str(uuid.uuid4())
root_element_nid = str(uuid.uuid4())
json_body = """
{"id": "00000000-0000-0000-0000-000000000000", "bal_Num": null, "beg_Bal": null, "cmte_Id": "", "dist_No": null, 
"end_Bal": null, "intr_ST": "", "tran_Id": "PAY107", "tran_ST": "", "tres_ST": "", "amt_Paid": null, "bal_Name": null, 
"int_Rate": null, "intr_Emp": null, "intr_Occ": null, "juris_Cd": null, "latitude": null, "rec_Type": "LOAN",
"tran_Emp": "", "tran_Occ": "Tester", "amt_Incur": null, "bal_Juris": null, "cand_NamF": null, "cand_NamL": null, 
"cand_NamS": null, "cand_NamT": null, "elec_Date": null, "entity_Cd": "IND", "form_Type": "B1", "intr_Adr1": "", 
"intr_Adr2": "", "intr_City": "", "intr_NamF": "", "intr_NamL": "", "intr_NamS": "", "intr_NamT": "", 
"intr_Self": false, "intr_Zip4": "", "loan_Amt1": 0.0, "loan_Amt2": 1000.0, "loan_Amt3": 0.0, "loan_Amt4": 1000.0, 
"loan_Amt5": 0.0, "loan_Amt6": 0.0, "loan_Amt7": 0.0, "loan_Amt8": 1000.0, "loan_Rate": "0.00", "longitude": null, 
"memo_Code": false, "office_Cd": null, "tran_Adr1": "", "tran_Adr2": "", "tran_Amt1": null, "tran_Amt2": null, 
"tran_City": "", "tran_Code": null, "tran_Date": null, "tran_Dscr": null, "tran_NamF": "Kansen", "tran_NamL": "Chu",
"tran_NamS": "", "tran_NamT": "", "tran_Self": false, "tran_Type": null, "tran_Zip4": "", "tres_Adr1": "", 
"tres_Adr2": "", "tres_City": "", "tres_NamF": "", "tres_NamL": "", "tres_NamS": "", "tres_NamT": "", "tres_Zip4": "",
"amountType": "NotApplicable", "bakRef_TID": "", "externalId": null, "g_From_E_F": null, "int_CmteId": null, 
"juris_Dscr": null, "loan_Date1": "2016-12-31T00:00:00", "loan_Date2": "2017-12-31T00:00:00", "memo_RefNo": "", 
"off_S_H_Cd": null, "sequenceId": 0, "sup_Opp_Cd": null, "tran_ChkNo": null, "tran_Date1": null, "xref_Match": false,
"lender_Name": null, "office_Dscr": null, "xref_SchNum": null, "calculated_Date": "2016-12-31T00:00:00", 
"calculated_Amount": 0.0, "calTransactionType": "F460B1"}"""
element = {'elementNid': element_nid, 'rootElementNid': root_element_nid,
           'filingNid': filing_nid, 'rootFilingNid': root_filing_nid, 'specificationKey': specification_key,
           'elementClassification': element_classification, 'elementType': element_type,
           'elementIndex': element_index, 'elementModel': json_body}

element_activity = ElementActivityV101(str(uuid.uuid4()), api_version, creation_date, filing_activity_nid,
                                       activity_type, publish_sequence, element)

identity_id = str(uuid.uuid4())
feed_id = str(uuid.uuid4())
active_sync_subscription = SyncSubscription(str(uuid.uuid4()), version, identity_id, feed_id, 'Test Feed', False, 'Active')
canceled_sync_subscription = SyncSubscription(str(uuid.uuid4()), 1, identity_id, feed_id, 'Test Feed', False, 'canceled')

#!/usr/bin/python

import json


class FilingActivityV101:
    def __init__(self, filing_activity_nid, api_version, creation_date, last_update, activity_type, publish_sequence,
                 filing):
        self.filing_activity_nid = filing_activity_nid
        self.api_version = api_version
        self.creation_date = creation_date
        self.last_update = last_update
        self.activity_type = activity_type
        self.publish_sequence = publish_sequence
        self.filing = FilingV101(filing['filingNid'], filing['rootFilingNid'], filing['filingMeta'],
                                 filing['filerMeta'], filing['agencyMeta'])

    def __str__(self):
        """Returned when this class is called by a print statement."""
        return f"Type: {self.activity_type}"


class FilingV101:
    def __init__(self, filing_nid, root_filing_nid, filing_meta, filer_meta, agency_meta):
        self.filing_nid = filing_nid
        self.root_filing_nid = root_filing_nid
        self.filing_meta = FilingMeta(filing_meta['legalOrigin'], filing_meta['legalFilingId'],
                                      filing_meta['specificationKey'], filing_meta['formId'],
                                      filing_meta['legalFilingDate'], filing_meta['startDate'], filing_meta['endDate'],
                                      filing_meta['reportNumber'], filing_meta['applyToLegalFilingId'])
        self.filer_meta = FilerMeta(filer_meta['longId'], filer_meta['stringId'], filer_meta['commonName'],
                                    filer_meta['systemizedName'], filer_meta['status'], filer_meta['phoneList'],
                                    filer_meta['emailList'], filer_meta['addressList'])
        self.agency_meta = AgencyMeta(agency_meta['aid'], agency_meta['clientDataspaceId'],
                                      agency_meta['applicationDataspaceId'])


class FilingMeta:
    def __init__(self, legal_origin, legal_filing_id, specification_key, form_id, legal_filing_date, start_date,
                 end_date, report_number, apply_to_legal_filing_id):
        self.legal_origin = legal_origin
        self.legal_filing_id = legal_filing_id
        self.specification_key = specification_key
        self.form_id = form_id
        self.legal_filing_date = legal_filing_date
        self.start_date = start_date
        self.end_date = end_date
        self.report_number = report_number
        self.apply_to_legal_filing_id = apply_to_legal_filing_id


class FilerMeta:
    def __init__(self, long_id, string_id, common_name, systemized_name, status, phone_list, email_list, address_list):
        self.long_id = long_id
        self.string_id = string_id
        self.common_name = common_name
        self.systemized_name = systemized_name
        self.status = status
        self.phone_list = phone_list
        self.email_list = email_list
        self.address_list = address_list


class AgencyMeta:
    def __init__(self, aid, client_dataspace_id, application_dataspace_id):
        self.aid = aid
        self.client_dataspace_id = client_dataspace_id
        self.application_dataspace_id = application_dataspace_id


class ElementActivityV101:
    def __init__(self, element_activity_nid, api_version, creation_date, filing_activity_nid, activity_type,
                 publish_sequence, element):
        self.element_activity_nid = element_activity_nid
        self.api_version = api_version
        self.creation_date = creation_date
        self.filing_activity_nid = filing_activity_nid
        self.activity_type = activity_type
        self.publish_sequence = publish_sequence
        self.filing_element = FilingElementV101(element['elementNid'], element['rootElementNid'], element['filingNid'],
                                                element['rootFilingNid'], element['specificationKey'],
                                                element['elementClassification'], element['elementType'],
                                                element['elementIndex'], json.dumps(element['elementModel']))


class FilingElementV101:
    def __init__(self, element_nid, root_element_nid, filing_nid, root_filing_nid, specification_key,
                 element_classification, element_type, element_index, element_model):
        self.element_nid = element_nid
        self.root_element_nid = root_element_nid
        self.filing_nid = filing_nid
        self.root_filing_nid = root_filing_nid
        self.specification_key = specification_key
        self.element_classification = element_classification
        self.element_type = element_type
        self.element_index = element_index
        self.element_model = element_model


class SystemReport:
    """
    System Report describing status and System Component information

    :param name: System name
    :param general_status: General status over the system
    :param components: System Components of this system
    """

    def __init__(self, name, general_status, components):
        self.name = name
        self.general_status = general_status
        self.components = []
        for component in components:
            name = component['name']
            status = component['status']
            build_version = component['buildVersion']
            build_vcs_name = component['buildVcsName']
            build_date_time = component['buildDateTime']
            message = component['message']
            self.components.append(SystemComponentInfo(name, status, build_version, build_vcs_name, build_date_time, message))

    def is_ready(self):
        return self.general_status == 'Ready'


class SystemComponentInfo:
    """
    SystemComponentInfo System Component Info describing status and build information
    :param name: Name of the component
    :param status: Status of the component
    :param build_version: Build version (from the assembly)
    :param build_vcs_name: VCS Name (typically a tag or branch name
    :param build_date_time: DateTime assembly was built
    :param message: General message
    """

    def __init__(self, name, status, build_version, build_vcs_name, build_date_time, message):
        self.name = name
        self.status = status
        self.build_version = build_version
        self.build_vcs_name = build_vcs_name
        self.build_date_time = build_date_time
        self.message = message


class ListQueryResult:
    def __init__(self, results, offset, has_previous_page, has_next_page, limit, total_count, empty, count, page_number):
        self.results = results
        self.offset = offset
        self.hasPreviousPage = has_previous_page
        self.hasNextPage = has_next_page
        self.limit = limit
        self.totalCount = total_count
        self.empty = empty
        self.count = count
        self.page_number = page_number

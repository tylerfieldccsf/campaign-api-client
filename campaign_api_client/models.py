#!/usr/bin/python

from enum import Enum


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


class FilingActivityType(Enum):
    New = 1
    Attach = 2
    Amend = 3
    Correct = 4
    Replace = 5
    Reparse = 6
    Delete = 7


class FilingActivityV1:
    """
    FilingActivityV1 does blah, blah
    :param id_arg: integer filing activity identifier
    :param version: description of arg
    :param creation_date: description of arg
    :param last_update: description of arg
    :param filing_activity_type: description of arg
    :param filing_specification_key: description of arg
    :param origin: description of arg
    :param origin_filing_id: description of arg
    :param agency_id: description of arg
    :param apply_to_filing_id: description of arg
    :param publish_sequence: description of arg
    """

    def __init__(self, id_arg, version, creation_date, last_update, filing_activity_type, filing_specification_key,
                 origin, origin_filing_id, agency_id, apply_to_filing_id, publish_sequence):
        """Class constructor"""
        self.id = id_arg
        self.version = version
        self.creation_date = creation_date
        self.last_update = last_update
        self.filing_activity_type = filing_activity_type
        self.filing_specification_key = filing_specification_key
        self.origin = origin
        self.origin_filing_id = origin_filing_id
        self.agency_id = agency_id
        self.apply_to_filing_id = apply_to_filing_id
        self.publish_sequence = publish_sequence

    def __str__(self):
        """Returned when this class is called by a print statement."""
        return "Activity Type: {activityType}, origin: {origin} ID: {id}".format(activityType=self.filing_activity_type, origin=self.origin, id=self.id)


class FilingElementV1:
    """
    FlilingElementV1 does blah, blah
    :param id_arg: integer filing activity identifier
    :param creation_date: integer filing activity identifier
    :param activity_id: integer filing activity identifier
    :param filing_activity_type: integer filing activity identifier
    :param filing_specification: integer filing activity identifier
    :param origin: integer filing activity identifier
    :param origin_filing_id: integer filing activity identifier
    :param agency_id: integer filing activity identifier
    :param apply_to_filing_id: integer filing activity identifier
    :param publish_sequence: integer filing activity identifier
    :param element_specification: integer filing activity identifier
    :param element_index: integer filing activity identifier
    :param model_json: integer filing activity identifier
    """

    def __init__(self, id_arg, creation_date, activity_id, filing_activity_type, filing_specification_key, origin,
                 origin_filing_id, agency_id, apply_to_filing_id, publish_sequence, element_specification,
                 element_index, model_json):
        self.id = id_arg
        self.creation_date = creation_date
        self.activity_id = activity_id
        self.filing_activity_type = filing_activity_type
        self.filing_specification_key = filing_specification_key
        self.origin = origin
        self.origin_filing_id = origin_filing_id
        self.agency_id = agency_id
        self.apply_to_filing_id = apply_to_filing_id
        self.publish_sequence = publish_sequence
        self.element_specification = element_specification
        self.element_index = element_index
        self.model_json = model_json


# class ContentLinkType(Enum):
#     Cafs = 1
#     PostgresLargeObject = 2
#     Http = 3
#     Other = 4
#
#
# class ContentLink:
#     """
#     ContentLink does blah, blah
#     :param name: description of arg
#     :param media_type: description of arg
#     :param link_type: description of arg
#     :param address: description of arg
#     """
#
#     def __init__(self, name, media_type, link_type, address):
#         """Class constructor"""
#         self.name = name
#         self.media_type = media_type
#         self.link_type = link_type
#         self.address = address


class SystemReport:
    """
    SystemReport does blah, blah
    :param name: description of arg
    :param general_status: description of arg
    :param components: description of arg
    """

    def __init__(self, name, general_status, components):
        """Class constructor"""
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


class SystemComponentInfo:
    """
    SystemComponentInfo does blah, blah
    :param name: description of arg
    :param status: description of arg
    :param build_version: description of arg
    :param build_vcs_name: description of arg
    :param build_date_time: description of arg
    :param message: description of arg
    """

    def __init__(self, name, status, build_version, build_vcs_name, build_date_time, message):
        """Class constructor"""
        self.name = name
        self.status = status
        self.build_version = build_version
        self.build_vcs_name = build_vcs_name
        self.build_date_time = build_date_time
        self.message = message

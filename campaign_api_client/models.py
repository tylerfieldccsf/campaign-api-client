#!/usr/bin/python

from enum import Enum


class FilingActivityType(Enum):
    New = 1
    Attach = 2
    Amend = 3
    Correct = 4
    Replace = 5
    Reparse = 6
    Delete = 7


class ContentLinkType(Enum):
    Cafs = 1
    PostgresLargeObject = 2
    Http = 3
    Other = 4


class FilingActivity:
    """
    FilingActivity does blah, blah
    :param id: integer filing activity identifier
    :param version: description of arg
    :param filing_sequence: description of arg
    :param creation_date: description of arg
    :param last_update: description of arg
    :param origin: description of arg
    :param original_filing_id: description of arg
    :param specification_key: description of arg
    :param activity_type: description of arg
    :param content: description of arg
    """

    def __init__(self, id_arg, version, filing_sequence, creation_date, last_update, origin, original_filing_id,
                 specification_key, activity_type, content):
        """Class constructor"""
        self.id = id_arg
        self.version = version
        self.filing_sequence = filing_sequence
        self.creation_date = creation_date
        self.last_update = last_update
        self.origin = origin
        self.original_filing_id = original_filing_id
        self.specification_key = specification_key
        self.activity_type = activity_type
        self.content = content

    def __str__(self):
        """Returned when this class is called by a print statement."""
        return "Activity Type: {activityType}, origin: {origin} ID: {id}".format(activityType=self.activity_type, origin=self.origin, id=self.id)


class ImmutableFiling:
    """
    ImmutableFiling does blah, blah
    :param id: integer filing activity identifier
    :param version: description of arg
    :param filing_sequence: description of arg
    :param creation_date: description of arg
    :param last_update: description of arg
    :param origin: description of arg
    :param original_filing_id: description of arg
    :param specification_key: description of arg
    :param content: description of arg
    """

    def __init__(self, id_arg, version, filing_sequence, creation_date, last_update, origin, original_filing_id,
                 specification_key, content):
        """Class constructor"""
        self.id = id_arg
        self.version = version
        self.filing_sequence = filing_sequence
        self.creation_date = creation_date
        self.last_update = last_update
        self.origin = origin
        self.original_filing_id = original_filing_id
        self.specification_key = specification_key
        self.content = content

    def __str__(self):
        """Returned when this class is called by a print statement."""
        return "Content: {content}, origin: {origin} ID: {id}".format(content=self.content, origin=self.origin, id=self.id)


class ContentLink:
    """
    ContentLink does blah, blah
    :param name: description of arg
    :param media_type: description of arg
    :param link_type: description of arg
    :param address: description of arg
    """

    def __init__(self, name, media_type, link_type, address):
        """Class constructor"""
        self.name = name
        self.media_type = media_type
        self.link_type = link_type
        self.address = address


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

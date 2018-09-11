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


class SpecificationRef:
    def __init__(self, org, name, version):
        self.org = org
        self.name = name
        self.version = version


class FlareActivity:
    """
    FlareActivity does blah, blah
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


class FlareElement:
    """
    FlareElement does blah, blah
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

    def __init__(self, id_arg, creation_date, activity_id, filing_activity_type, filing_specification, origin,
                 origin_filing_id, agency_id, apply_to_filing_id, publish_sequence, element_specification,
                 element_index, model_json):
        self.id = id_arg
        self.creation_date = creation_date
        self.activity_id = activity_id
        self.filing_activity_type = filing_activity_type
        self.filing_specification = filing_specification
        self.origin = origin
        self.origin_filing_id = origin_filing_id
        self.agency_id = agency_id
        self.apply_to_filing_id = apply_to_filing_id
        self.publish_sequence = publish_sequence
        self.element_specification = element_specification
        self.element_index = element_index
        self.model_json = model_json


class ContentLinkType(Enum):
    Cafs = 1
    PostgresLargeObject = 2
    Http = 3
    Other = 4


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


class SyncSubscriptionCommand:
    """
    SyncSubscriptionCommand is used to create, edit, and cancel SyncSubscriptions
    :param id_arg: Unique Id of the Subscription
    :param command_type: provides directive to create, edit, or cancel a subscription
    :param version: Version number of the Subscription, required for command execution and incremented after a successful command
    :param permission_name: name of permission
    """
    def __init__(self, id_arg, command_type, version, permission_name):
        self.id = id_arg
        self.command_type = command_type
        self.version = version
        self.permission_name = permission_name


class SyncSubscriptionResponse:
    """
        SyncSubscriptionResponse is returned after sending a SyncSubscriptionCommand
        :param execution_id: Id of the execution the command was performed withing
        :param command_type: The type of command executed
        :param subscription: Representation of the SyncSubscription after the command was executed
        :param description: Description of the command performed
        """
    def __init__(self, execution_id, command_type, subscription, description):
        self.execution_id = execution_id
        self.command_type = command_type
        self.subscription = subscription
        self.description = description


class SyncSubscriptionCommandType(Enum):
    Unknown = 1
    Create = 2
    Edit = 3
    Cancel = 4


class SyncSessionCommand:
    """
    SyncSessionCommand is used to create, record a read, complete, and cancel a SyncSession
    :param id_arg: Unique Id of the SyncSession
    :param command_type: The type of command to execute
    :param version: Version number of the SyncSession, required for command execution and incremented after a successful command
    :param permission_name: name of permission
    """
    def __init__(self, id_arg, command_type, description, version, permission_name):
        self.id = id_arg
        self.command_type = command_type
        self.description = description
        self.version = version
        self.permission_name = permission_name


class SyncSessionResponse:
    """
    Response returned from execution of a SynSession Command
    :param execution_id: Id of the execution the command was performed withing
    :param command_type: The type of command executed
    :param session: Representation of the SyncSession after the command was executed
    :param description: Description of the command performed
    """
    def __init__(self, execution_id, command_type, session, description):
        self.execution_id = execution_id
        self.command_type = command_type
        self.session = session
        self.description = description


class SyncSessionCommandType(Enum):
    Unknown = 1
    Create = 2
    RecordRead = 3
    Complete = 4
    Cancel = 5


class SyncFeed:
    """
    A Feed is a set of logically related data (Topics) which is published and available for synchronization
    :param id_arg: Unique Id of the Feed
    :param version: Version number of the Feed, required for command execution and incremented after a successful command
    :param product_type: Product the feed originates from
    :param api_version: Version of the API this Feed originates from
    :param name: Name of the feed
    :param description: Description of the feed
    :param status: Status of the Feed (Active, Canceled)
    :param topics: List of one or more Topic supported by the Feed. Reads are performed for a specific Topic
    """
    def __init__(self, id_arg, version, product_type, api_version, name, description, status, topics):
        self.id_arg = id_arg
        self.version = version
        self.product_type = product_type
        self.api_version = api_version
        self.name = name
        self.description = description
        self.status = status
        self.topics = topics


class SyncFeedCommand:
    """
    :param id_arg: Unique Id of the Feed
    :param command_type: Create, Edit, or Cancel a sync feed
    :param version: Version number of the Feed, required for command execution and incremented after a successful command
    :param permission_name: Name of permission
    """
    def __init__(self, id_arg, command_type, version, permission_name):
        self.id = id_arg
        self.command_type = command_type
        self.version = version
        self.permission_name = permission_name


class SyncTopic:
    """
    A Topic is a specific data set defined with a Feed available for read. In most cases data within a Topic will utilize one common structure
    :param name: Name of the Topic
    :param description: Description of the Topic
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description


class SyncFeedStatus(Enum):
    Active = 1
    Canceled = 2


class ProductType(Enum):
    Undefined = 1
    ProTreasurer = 2
    UnitTest = 3
    Sample = 4
    Nessy = 5
    Corsair = 6
    Lobby50 = 7
    Smc = 8
    NfBoot = 9
    CalAccess = 10
    Connect = 11
    CampaignDirectory = 12
    PubFi = 13
    Filing = 14
    Lobbyist = 15

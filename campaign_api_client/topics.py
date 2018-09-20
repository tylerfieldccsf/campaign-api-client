#!/usr/bin/python


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


class FilingActivityV101:
    def __init__(self, id_arg, version, api_version, creation_date, last_update, activity_type, specification_key,
                 origin, filing_id, aid, apply_to_filing_id, publish_sequence):
        self.id = id_arg
        self.version = version
        self.api_version = api_version
        self.creation_date = creation_date
        self.last_update = last_update
        self.activity_type = activity_type
        self.specification_key = specification_key
        self.origin = origin
        self.filing_id = filing_id
        self.aid = aid
        self.apply_to_filing_id = apply_to_filing_id
        self.publish_sequence = publish_sequence

    def __str__(self):
        """Returned when this class is called by a print statement."""
        return "Activity Type: {activityType}, origin: {origin} ID: {id}".format(activityType=self.activity_type, origin=self.origin, id=self.id)


class FilingActivityElementV101:
    def __init__(self, id_arg, api_version, creation_date, activity_id, activity_type, specification_key, origin,
                 origin_filing_id, agency_id, apply_to_filing_id, publish_sequence, element_type,
                 element_index, model_json):
        self.id = id_arg
        self.api_version = api_version
        self.creation_date = creation_date
        self.activity_id = activity_id
        self.activity_type = activity_type
        self.specification_key = specification_key
        self.origin = origin
        self.origin_filing_id = origin_filing_id
        self.agency_id = agency_id
        self.apply_to_filing_id = apply_to_filing_id
        self.publish_sequence = publish_sequence
        self.element_type = element_type
        self.element_index = element_index
        self.model_json = model_json


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

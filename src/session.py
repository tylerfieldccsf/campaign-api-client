#!/usr/bin/python

from enum import Enum


class SyncSession:
    """
    A SyncSession acts as the context for synchronization within a feed for a client. The Session defines a data range
    ensuring consistent reads across all Topics within the Feed

    :param id_arg: Unique Id of the SyncSession
    :param version: Version number of the SyncSession, required for command execution and incremented after a successful command
    :param subscription_id: Id of the SyncSubscription this SyncSession is for
    :param identity_id: Id of the Identity/Client
    :param status: Status of the Session {Active, Completed, Canceled)
    :param sequence_range_begin: Begin sequence number, when a sequence range is used
    :param sequence_range_end: End sequence number, when a sequence range is used
    :param started_at: Datetime the session was started
    :param ended_at: DateTime the session was ended (may be null if session is still Active)
    :param reads: The list of Reads which requests which have been performed within this session
    """
    def __init__(self, id_arg, version, subscription_id, identity_id, status, sequence_range_begin, sequence_range_end,
                 started_at, ended_at, reads):
        self.id = id_arg
        self.version = version
        self.subscription_id = subscription_id
        self.identity_id = identity_id
        self.status = status
        self.sequence_range_begin = sequence_range_begin
        self.sequence_range_end = sequence_range_end
        self.started_at = started_at
        self.ended_at = ended_at
        self.reads = reads

    def __str__(self):
        output = f'SyncSession: id={self.id}, version={self.version}, subscription_id={self.subscription_id}, '
        output += f'identity_id={self.identity_id}, status={self.status}, '
        output += f'sequence_range_begin={self.sequence_range_begin}, sequence_range_end={self.sequence_range_end}, '
        output += f'started_at={self.started_at}, ended_at={self.ended_at}'
        return output


class SyncSessionRead:
    """
    A SyncSessionRead records the details of a read operation within a Topic and Feed for a client

    :param topic: The topic the read was performed for
    :param limit: Max number of records to return in the IQueryResult
    :param offset: Offset into the overall result set (used for paging)
    :param result_count: Number of records returned in the IQueryResult response
    :param total_count: Total number of records available for read within the topic and with any filters applied
    :param executed_at: Date time the read was performed
    """
    def __init__(self, topic, limit, offset, result_count, total_count, executed_at):
        self.topic = topic
        self.limit = limit
        self.offset = offset
        self.result_count = result_count
        self.total_count = total_count
        self.executed_at = executed_at


class SyncSessionStatus(Enum):
    Active = 1
    Completed = 2
    Canceled = 3


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


class CreateSyncSessionResponse:
    """
    Response returned from execution of a Create SynSession Command

    :param sync_data_available: True if new data is available for sync
    :param session: SyncSession created by the command or null if no new data available and a session was not created
    :param description: Description of the command performed
    :param topic_links: List of topic links which can be used to read topics within the context of this session
    """
    def __init__(self, sync_data_available, session, description, topic_links):
        self.sync_data_available = sync_data_available
        self.topic_links = topic_links
        self.session = session if session is None else SyncSession(session['id'], session['version'], session['subscriptionId'],
                                   session['identityId'], session['status'], session['sequenceRangeBegin'], session['sequenceRangeEnd'],
                                   session['startedAt'], session['endedAt'], session['reads'])
        self.description = description


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
        self.session = SyncSession(session['id'], session['version'], session['subscriptionId'], session['identityId'],
                                   session['status'], session['sequenceRangeBegin'], session['sequenceRangeEnd'],
                                   session['startedAt'], session['endedAt'], session['reads'])
        self.description = description


class SyncSessionCommandType(Enum):
    Unknown = 1
    Create = 2
    RecordRead = 3
    Complete = 4
    Cancel = 5

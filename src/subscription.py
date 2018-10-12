#!/usr/bin/python

from enum import Enum


class SyncSubscription:
    """
    A Subscription represents the detailed state and configuration for data synchronization for a specific feed
    and identity/user.

    :param id_arg: Unique Id of the Subscription
    :param version: Version number of the Subscription, required for command execution and incremented after a successful command
    :param identity_id: Id of the Identity who created/owns the Subscription
    :param feed_id: Id of the Feed the Subscription is for
    :param name: Name of the Subscription - informational only
    :param auto_complete: If true SynSessions created for this Subscription will be assigned status of Completed as soon as it is created. Defaults to false, can be overriden at SyncSession creation time
    :param status: Status of the Subscription
    """
    def __init__(self, id_arg, version, identity_id, feed_id, name, auto_complete, status):
        self.id = id_arg
        self.version = version
        self.identity_id = identity_id
        self.feed_id = feed_id
        self.name = name
        self.auto_complete = auto_complete
        self.status = status

    def __str__(self):
        return f'Subscription Name: {self.name}, Status: {self.status}, ID: {self.id}, Version: {self.version}'


class SyncSubscriptionStatus(Enum):
    Active = 1
    Canceled = 2


class SyncFilter:
    """
    A Filter represents custom selection criteria for a topic within a feed. Defined by the user within the Subscription

    :param topic_name: The name of the Topic the Filer applies to
    """
    def __init__(self, topic_name):
        self.topic_name = topic_name


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
        self.subscription = SyncSubscription(subscription['id'], subscription['version'], subscription['identityId'],
                                             subscription['feedId'], subscription['name'], subscription['autoComplete'],
                                             subscription['status'])
        self.description = description


class SyncSubscriptionCommandType(Enum):
    Unknown = 1
    Create = 2
    Edit = 3
    Cancel = 4

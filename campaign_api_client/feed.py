#!/usr/bin/python


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
        self.id = id_arg
        self.version = version
        self.product_type = product_type
        self.api_version = api_version
        self.name = name
        self.description = description
        self.status = status
        self.topics = []
        for topic in topics:
            self.topics.append(SyncTopic(topic['name'], topic['description']))

    def __str__(self):
        output = f'Feed Id: {self.id}, Feed Name: {self.name}, Topics: '
        for topic in self.topics:
            output += f'\n\tTopic Name: {topic.name} Description: {topic.description}'
        return output


class SyncFeedResponse:
    """
    Response return from execution of a SyncFeed Command
    :param execution_id: Id of the execution the command was performed withing
    :param command_type: The type of command executed
    :param feed: Representation of the SyncFeed after the command was executed
    :param description: Description of the command performed
    """
    def __init__(self, execution_id, command_type, feed, description):
        self.execution_id = execution_id
        self.command_type = command_type
        self.feed = SyncFeed(feed.id, feed.version, feed.product_type, feed.api_version, feed.name,
                             feed.description, feed.status, feed.topics)
        self.description = description


class SyncTopic:
    """
    A Topic is a specific data set defined with a Feed available for read. In most cases data within a Topic will utilize one common structure
    :param name: Name of the Topic
    :param description: Description of the Topic
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description

#!/usr/bin/python

import requests
import logging
from models import SystemReport


class CampaignApiHttpClient:
    """Provides support for synchronizing local database with Campaign API filing data"""
    def __init__(self, base_url):
        self.headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        self.base_url = base_url

    def fetch_system_report(self):
        url = self.base_url + Routes.SYSTEM_REPORT
        response = requests.get(url, headers=self.headers)
        name = response.json()['name']
        general_status = response.json()['generalStatus']
        components = response.json()['components']
        system_report = SystemReport(name, general_status, components)
        logging.debug('General Status: %s', system_report.general_status)
        logging.debug('General Status: %s', system_report.name)
        for component in system_report.components:
            logging.debug('\tComponent Name: %s', component.name)
            logging.debug('\tComponent Message: %s', component.message)
            logging.debug('\tComponent status: %s', component.status)
            logging.debug('\tComponent Build DateTime: %s', component.build_date_time)
            logging.debug('\tComponent Build Version: %s', component.build_version)
        return system_report

    def create_subscription(self):
        pass

    def start_session(self):
        pass

    def end_session(self, session_id):
        pass

    def sync_topic(self, subscription_id, session_id, topic):
        pass


class Routes:
    SYSTEM_REPORT = "/system"

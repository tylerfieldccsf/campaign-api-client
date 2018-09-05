#!/usr/bin/python

import requests
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
        return SystemReport(name, general_status, components)

    def create_subscription(self):
        pass

    def start_session(self):
        pass

    def end_session(self):
        pass

    def start_sync(self):
        pass


class Routes:
    SYSTEM_REPORT = "/system"

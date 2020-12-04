# Copyright 2020 Clivern
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.oauth2.credentials
import googleapiclient.discovery

from .exception import APICallError
from .utils import credentials_to_dict
from .constant import Version
from .constant import Service


class Calendar():

    def get_events(self, calendarId='primary', filters={}):
        """
        Get Events

        Args:
            calendarId: the calendar ID
            filters: events filter

        Returns:
            Events list

        Raises:
            APICallError: If API call failed
        """
        filters['calendarId'] = calendarId
        credentials = google.oauth2.credentials.Credentials(**self.credentials)

        try:
            service = googleapiclient.discovery.build(
                Service.CALENDAR,
                Version.API_V3,
                credentials=credentials
            )

            result = service.events().list(**filters).execute()
            events = result.get('items', [])
        except Exception as e:
            raise APICallError("API error while fetching events: {}".format(str(e)))

        self.credentials = credentials_to_dict(credentials)

        return events

    def create_event(self, calendarId='primary', body={}):
        """
        Create Event

        Args:
            calendarId: the calendar ID
            body: event settings https://developers.google.com/calendar/v3/reference/events/insert

        Returns:
            The event that got created

        Raises:
            APICallError: If API call failed
        """
        body['calendarId'] = calendarId
        credentials = google.oauth2.credentials.Credentials(**self.credentials)

        try:
            service = googleapiclient.discovery.build(
                Service.CALENDAR,
                Version.API_V3,
                credentials=credentials
            )

            event = service.events().insert(**body).execute()
        except Exception as e:
            raise APICallError("API error while fetching events: {}".format(str(e)))

        self.credentials = credentials_to_dict(credentials)

        return event

    def set_credentials(self, credentials):
        """
        Set Credentials

        Args:
            credentials: the oauth credentials
        """
        self.credentials = credentials

    def get_credentials(self):
        """Get Credentials"""
        return self.credentials

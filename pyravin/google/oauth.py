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

import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from .constant import Service
from .constant import Version
from .constant import APIs
from .exception import APICallError
from .utils import credentials_to_dict


class OAuth():
    """OAuth Class"""

    def __init__(self, client_configs, scopes=[]):
        """Inits OAuth

        Args:
            client_configs: a dict of client configs

            scopes: List of scopes required
        """
        self.client_configs = client_configs
        self.scopes = scopes

    def get_authorization_url(self, redirect_uri):
        """
        Get Authorization URL

        Args:
            redirect_uri: Web application redirect uri for oauth callback

        Returns:
            Authorization URL and state value
        """
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            self.client_configs,
            scopes=self.scopes
        )

        # The URI created here must exactly match one of the authorized redirect URIs
        # for the OAuth 2.0 client, which you configured in the API Console. If this
        # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
        # error.
        flow.redirect_uri = redirect_uri

        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true'
        )

        return authorization_url, state

    def fetch_credentials(self, state, redirect_uri, request_url):
        """
        Get Credentials from request URL

        Args:
            state: Authorization state value
            redirect_uri: Web application redirect uri for oauth callback
            request_url: Current request URL

        Returns:
            a dict of credentials

        Raises:
            APICallError: If API call failed
        """
        try:
            flow = google_auth_oauthlib.flow.Flow.from_client_config(
                self.client_configs,
                scopes=self.scopes,
                state=state
            )

            flow.redirect_uri = redirect_uri

            # Use the authorization server's response to fetch the OAuth 2.0 tokens.
            flow.fetch_token(authorization_response=request_url)
        except Exception as e:
            raise APICallError("API error while fetching credentials: {}".format(str(e)))

        # Store credentials in the session or database
        credentials = flow.credentials

        self.credentials = credentials_to_dict(credentials)

        return self.credentials

    def get_user_info(self):
        """
        Get user info

        Returns:
            The user info. something like
            {
                "email": "test@clivern.com",
                "given_name": "Clivern",
                "hd": "clivern.com",
                "id": "10000000000000000000000000",
                "locale": "en",
                "name": "Clivern",
                "picture": "https://lh3.googleusercontent.com/a-/AOh14Gh8rjdYiSrh",
                "verified_email": true
            }

        Raises:
            APICallError: If API call failed
        """
        credentials = google.oauth2.credentials.Credentials(**self.credentials)

        try:
            service = googleapiclient.discovery.build(
                Service.OAuth,
                Version.API_V2,
                credentials=credentials
            )
            userinfo = service.userinfo().get().execute()
        except Exception as e:
            raise APICallError("API error while fetching userinfo: {}".format(str(e)))

        self.credentials = credentials_to_dict(credentials)

        return userinfo

    def revoke_credentials(self):
        """
        Revoke Credentials

        Returns:
            True on success and False on failure

        Raises:
            APICallError: If API call failed
        """
        credentials = google.oauth2.credentials.Credentials(**self.credentials)

        try:
            revoke = requests.post(
                APIs.REVOKE_CREDENTIALS,
                params={'token': credentials.token},
                headers={'content-type': 'application/x-www-form-urlencoded'}
            )
        except Exception as e:
            raise APICallError("API error while revoking credentials: {}".format(str(e)))

        status_code = getattr(revoke, 'status_code')

        if status_code == 200:
            return True
        else:
            return False

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

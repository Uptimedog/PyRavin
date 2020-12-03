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
from .constant import API_VERSION
from .constant import OAUTH_SERVICE_NAME
from .constant import OAUTH_REVOKE_API


class OAuth():

    def __init__(self, client_configs, redirect_uri, scopes=[]):
        self.client_configs = client_configs
        self.redirect_uri = redirect_uri
        self.scopes = scopes

    def get_authorization_url(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            self.client_configs,
            scopes=self.scopes
        )

        # The URI created here must exactly match one of the authorized redirect URIs
        # for the OAuth 2.0 client, which you configured in the API Console. If this
        # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
        # error.
        flow.redirect_uri = self.redirect_uri

        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true'
        )

        return authorization_url, state

    def get_credentials(self, state, request_url):
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            self.client_configs,
            scopes=self.scopes,
            state=state
        )

        flow.redirect_uri = self.redirect_uri

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = request_url

        flow.fetch_token(authorization_response=authorization_response)

        # Store credentials in the session.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        credentials = flow.credentials

        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

    def get_user_info(self, credentials):
        """
        Get user info

        Args:
            credentials: a dict of credentials

        Returns

            New credentials and user info for example
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
        """
        credentials = google.oauth2.credentials.Credentials(**credentials)

        userinfo_service = googleapiclient.discovery.build(OAUTH_SERVICE_NAME, API_VERSION, credentials=credentials)
        userinfo = userinfo_service.userinfo().get().execute()

        new_credentials = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

        return new_credentials, userinfo

    def revoke_credentials(self, credentials):
        credentials = google.oauth2.credentials.Credentials(**credentials)

        revoke = requests.post(
            OAUTH_REVOKE_API,
            params={'token': credentials.token},
            headers={'content-type': 'application/x-www-form-urlencoded'}
        )

        status_code = getattr(revoke, 'status_code')

        if status_code == 200:
            return True
        else:
            return False

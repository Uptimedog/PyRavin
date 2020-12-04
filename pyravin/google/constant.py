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


class Version():
    API_V2 = 'v2'
    API_V3 = 'v3'


class Scope():
    OPENID = 'openid'
    USERINFO_EMAIL = 'https://www.googleapis.com/auth/userinfo.email'
    USERINFO_PROFILE = 'https://www.googleapis.com/auth/userinfo.profile'
    CALENDAR_READ_OLNY = 'https://www.googleapis.com/auth/calendar.readonly'
    CALENDAR = 'https://www.googleapis.com/auth/calendar'


class Service():
    OAuth = 'oauth2'
    CALENDAR = 'calendar'


class APIs():
    REVOKE_CREDENTIALS = 'https://oauth2.googleapis.com/revoke'

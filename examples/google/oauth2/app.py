import os
import flask

from pyravin.google.oauth import OAuth
from pyravin.google.calendar import Calendar
from pyravin.google.constant import Scope


app = flask.Flask(__name__)
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

configs = {
    "web": {
        "client_id":"22222222222.apps.googleusercontent.com",
        "project_id":"pyraven",
        "auth_uri":"https://accounts.google.com/o/oauth2/auth",
        "token_uri":"https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
        "client_secret":"4444444444444",
        "redirect_uris":[
            "https://33333.ngrok.io",
            "http://4444.ngrok.io",
            "https://3334433.ngrok.io/oauth2callback",
            "http://444444.ngrok.io/oauth2callback"
        ]
    }
}

scopes = [Scope.OPENID, Scope.USERINFO_EMAIL, Scope.USERINFO_PROFILE, Scope.CALENDAR]

oauth = OAuth(configs, scopes)

def print_index_table():
    return ('<table>' +
        '<tr><td><a href="/test">Test an API request</a></td>' +
        '<tr><td><a href="/get-calendar-events">Get Calendar Events</a></td>' +
        '<tr><td><a href="/create-calendar-event">Create Calendar Event</a></td>' +
        '<td>Submit an API request and see a formatted JSON response. ' +
        '    Go through the authorization flow if there are no stored ' +
        '    credentials for the user.</td></tr>' +
        '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
        '<td>Go directly to the authorization flow. If there are stored ' +
        '    credentials, you still might not be prompted to reauthorize ' +
        '    the application.</td></tr>' +
        '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
        '<td>Revoke the access token associated with the current user ' +
        '    session. After revoking credentials, if you go to the test ' +
        '    page, you should see an <code>invalid_grant</code> error.' +
        '</td></tr>' +
        '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
        '<td>Clear the access token currently stored in the user session. ' +
        '    After clearing the token, if you <a href="/test">test the ' +
        '    API request</a> again, you should go back to the auth flow.' +
        '</td></tr></table>')


@app.route('/')
def index():
    return print_index_table()


@app.route('/test')
def test_api_request():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    oauth.set_credentials(flask.session['credentials'])
    userinfo = oauth.get_user_info()

    flask.session['credentials'] = oauth.get_credentials()

    return flask.jsonify(**userinfo)


@app.route('/get-calendar-events')
def test_get_calendar_events():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    calendar = Calendar()
    calendar.set_credentials(flask.session['credentials'])
    events = calendar.get_events()

    flask.session['credentials'] = calendar.get_credentials()

    return flask.jsonify(**{"events": events})


@app.route('/create-calendar-event')
def test_create_calendar_event():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    calendar = Calendar()
    calendar.set_credentials(flask.session['credentials'])

    event = calendar.create_event("primary", {
        "sendUpdates": "all",
        # Create google meet link
        "conferenceDataVersion": 1,

        "body": {
            "end": {
                "dateTime": "2020-12-05T20:00:00-07:00",
                "timeZone": "America/Los_Angeles"
            },
            "start": {
                "dateTime": "2020-12-05T18:00:00-07:00",
                "timeZone": "America/Los_Angeles"
            },
            "attendees": [
                {
                    "email": "test@clivern.com"
                },
                {
                    "email": "test@gmail.com"
                },
                {
                    "email": "test@outlook.com"
                }
            ],
            "description": "A chance to hear more about Google's developer products.",
            "summary": "Google I/O 2020",
            "location": "800 Howard St., San Francisco, CA 94103",

            # Create google meet link
            "conferenceData": {
                "createRequest": {
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    },
                    "requestId": "dghwtet344"
                }
            }
        }
    })

    flask.session['credentials'] = calendar.get_credentials()

    return flask.jsonify(**{"event": event})


@app.route('/authorize')
def authorize():
    auth_url, state = oauth.get_authorization_url(flask.url_for('oauth2callback', _external=True))

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(auth_url)


@app.route('/oauth2callback')
def oauth2callback():
    flask.session['credentials'] = oauth.fetch_credentials(
        flask.session['state'],
        flask.url_for('oauth2callback', _external=True),
        flask.request.url
    )

    return flask.redirect(flask.url_for('test_api_request'))


@app.route('/revoke')
def revoke():
    if 'credentials' not in flask.session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

    oauth.set_credentials(flask.session['credentials'])
    status = oauth.revoke_credentials()

    if status:
        return('Credentials successfully revoked.' + print_index_table())
    else:
        return('An error occurred.' + print_index_table())


@app.route('/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']

    return ('Credentials have been cleared.<br><br>' +
          print_index_table())


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.
    app.run('localhost', 8000, debug=True)

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
    "web" : {
        "client_id": "11111111-222222222.apps.googleusercontent.com",
        "project_id": "pyraven",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "MSCvp-111111111111111",
        "redirect_uris": [
            "https://222222ffffff.ngrok.io/oauth2callback",
            "http://222222ffffff.ngrok.io/oauth2callback",
            "https://222222ffffff.ngrok.io",
            "http://222222ffffff.ngrok.io"
        ]
    }
}
scopes = [Scope.OPENID, Scope.USERINFO_EMAIL, Scope.USERINFO_PROFILE, Scope.CALENDAR_READ_OLNY]

oauth = OAuth(configs, scopes)


def print_index_table():
    return ('<table>' +
        '<tr><td><a href="/test">Test an API request</a></td>' +
        '<tr><td><a href="/calendar">Get Calendar Events</a></td>' +
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

    flask.session['credentials'], userinfo = oauth.get_user_info(flask.session['credentials'])

    return flask.jsonify(**userinfo)


@app.route('/calendar')
def test_calendar_request():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    calendar = Calendar()

    flask.session['credentials'], events = calendar.get_events(flask.session['credentials'])

    return flask.jsonify(**{"events": events})


@app.route('/authorize')
def authorize():
    auth_url, state = oauth.get_authorization_url(flask.url_for('oauth2callback', _external=True))

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(auth_url)


@app.route('/oauth2callback')
def oauth2callback():
    flask.session['credentials'] = oauth.get_credentials(
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

    status = oauth.revoke_credentials(flask.session['credentials'])

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

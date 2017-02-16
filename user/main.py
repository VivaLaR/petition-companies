import logging
import os
import uuid

import flask
import httplib2
from shared import db
from oauth2client import client
import emails

app = flask.Flask(__name__)
app.secret_key = str(uuid.uuid4())

logger = logging.getLogger(__name__)

FILEPATH_CREDENTIALS = os.path.join(os.path.dirname(__file__), 'client_secret.json')
# Comes from https://developers.google.com/identity/protocols/googlescopes#gmailv1
SCOPE = ['https://www.googleapis.com/auth/gmail.send']
DT_FORMAT = '%m-%d-%Y %H:%M'

KEY_EMAIL_DICT = 'eid_rids_dict'
KEY_EMAIL_TXTS_DICT = 'email_txts_dict'
KEY_OAUTH_ORIG_FUNC = 'original_func_name'


@app.route('/')
def index():
    checked = flask.session.pop(KEY_EMAIL_DICT, default=None)
    advertisees = db.get_advertisees()
    return flask.render_template('index.html', advertisees=advertisees, checked=checked)


@app.route('/login')
def login():

    if 'credentials' not in flask.session:
        flask.session[KEY_OAUTH_ORIG_FUNC] = login.__name__
        return flask.redirect(flask.url_for('oauth2callback'))

    return flask.redirect(flask.url_for('index'))


@app.route('/email', methods=['GET', 'POST'])
def email():

    if flask.request.method == 'POST':
        eid_rids_dict = flask.request.form
        email_txts_dict = {k[6:]: eid_rids_dict.pop(k) for k in tuple(eid_rids_dict) if k[:6] == 'email_'}
        eid_rids_dict = {k: v.split(',') for k, v in eid_rids_dict.items()}

        if 'credentials' not in flask.session:
            flask.session[KEY_OAUTH_ORIG_FUNC] = email.__name__
            flask.session[KEY_EMAIL_DICT] = eid_rids_dict
            flask.session[KEY_EMAIL_TXTS_DICT] = email_txts_dict
            return flask.redirect(flask.url_for('oauth2callback'))
    else:
        eid_rids_dict = flask.session[KEY_EMAIL_DICT]
        email_txts_dict = flask.session[KEY_EMAIL_TXTS_DICT]

    http = _get_auth_http()
    emails.send_messages(eid_rids_dict, http, email_txts_dict)

    return flask.redirect(flask.url_for('index'))


def _get_auth_http():
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    h = credentials.authorize(httplib2.Http())

    return h


@app.route('/oauth2callback')
def oauth2callback():
    """
    Endpoint for both oauth steps.
    :return: Response to authorize or response to exchange auth code for access token.
    """
    flow = client.flow_from_clientsecrets(FILEPATH_CREDENTIALS,
                                          scope=SCOPE,
                                          redirect_uri=flask.url_for('oauth2callback', _external=True))
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        func_name = flask.session.get(KEY_OAUTH_ORIG_FUNC, 'index')
        return flask.redirect(flask.url_for(func_name))


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)

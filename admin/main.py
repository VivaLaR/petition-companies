from __future__ import print_function

import logging
import os
import uuid

import flask
from shared import db

app = flask.Flask(__name__)
app.secret_key = str(uuid.uuid4())

logger = logging.getLogger(__name__)

FILEPATH_CREDENTIALS = os.path.join(os.path.dirname(__file__), 'client_secret.json')
# Comes from https://developers.google.com/identity/protocols/googlescopes#gmailv1
SCOPE = ['https://www.googleapis.com/auth/gmail.send']
DT_FORMAT = '%m-%d-%Y %H:%M'

app.url_map.strict_slashes = False


@app.route('/admin')
def index():

    return flask.redirect(flask.url_for('advertisees'))


@app.route('/admin/advertisers')
def advertisers():

    advertisers = db.get_advertisers()

    print(advertisers)
    return flask.render_template('advertisers.html', advertisers=advertisers)


@app.route('/admin/advertiser', methods=['GET', 'POST', 'DELETE'])
@app.route('/admin/advertiser/<int:advertiser_id>', methods=['GET', 'POST', 'DELETE'])
def advertiser(advertiser_id=None):

    if flask.request.method == 'DELETE':
        db.delete_advertiser(advertiser_id)
        return '', 204

    if advertiser_id is not None:
        a = db.get_advertiser(advertiser_id)
    else:
        a = db.create_blank_advertiser()

    if flask.request.method == 'GET':
        return flask.render_template('advertiser.html', advertiser=a)
    else:
        advertiser_dict = flask.request.get_json()
        a.name = advertiser_dict['name']

        new_ = []
        changed = []
        deleted_poc_ids = [poc.id() for poc in a.pocs]
        for poc_id, poc_dict in advertiser_dict['pocs'].items():
            if poc_id != '':
                poc_id = int(poc_id)
                deleted_poc_ids.remove(poc_id)
                poc = db.create_poc()
                changed.append(poc)
            else:
                poc = db.create_poc()
                new_.append(poc)
            poc.name = poc_dict['name']
            poc.email = poc_dict['email']

        new_keys = db.put(new_)
        db.put(changed)
        db.delete(deleted_poc_ids, kind='POC')

        a.pocs = [x.key for x in changed] + new_keys

        a.put()

        return '', 204


@app.route('/admin/advertisees')
def advertisees():

    advertisees = db.get_advertisees()

    return flask.render_template('advertisees.html', advertisees=advertisees)


@app.route('/admin/advertisee/', methods=['GET', 'POST', 'DELETE'])
@app.route('/admin/advertisee/<int:advertisee_id>', methods=['GET', 'POST', 'DELETE'])
def advertisee(advertisee_id=None):

    if flask.request.method == 'DELETE':
        db.delete_advertisee(advertisee_id)
        return '', 204

    if advertisee_id is not None:
        a = db.get_advertisee(advertisee_id)
    else:
        a = db.create_blank_advertisee()

    if flask.request.method == 'GET':
        advertisers = db.get_advertisers(a.advertisers)
        advertisers_not_associated = [x for x in db.get_advertisers() if x.key not in a.advertisers]
        return flask.render_template('advertisee.html', advertisee=a, advertisers=advertisers, advertisers_not_associated=advertisers_not_associated)
    else:
        advertisee_dict = flask.request.get_json()
        a.name = advertisee_dict['name']
        a.description = advertisee_dict['description']
        a.email = advertisee_dict['email']

        a.put()

        return '', 204


@app.route('/admin/advertisee_advertiser', methods=['POST'])
def manage_advertisee_advertiser():

    json_dict = flask.request.get_json()
    method = json_dict['method']
    eid, rid = int(json_dict['advertisee_id']), int(json_dict['advertiser_id'])

    if method == 'delete':
        db.remove_advertiser(eid, rid)
    else:
        db.add_advertiser(eid, rid)

    return '', 204


@app.route('/admin/insert')
def insert():

    from shared.db import insert_advertisexs
    insert_advertisexs()
    return 'Donezo'


@app.route('/admin/insert/advertiser')
def insert_advertiser():

    from shared.db import insert_advertiser
    insert_advertiser()
    return 'Donezo'


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)

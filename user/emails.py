import base64
from email.mime.text import MIMEText
from shared import db

from googleapiclient.discovery import build

# Python API docs: https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#send
gmail_service = build('gmail', 'v1')


def send_messages(advertisee_advertiser_dict, http, emails_dict):

    messages = []

    for eid, rids in advertisee_advertiser_dict.items():

        e = db.get_advertisee(int(eid))
        rids = [int(r) for r in rids]
        rs = db.get(rids, 'Advertiser')
        msg = emails_dict.get(eid)

        messages += [get_message(e, r, msg) for r in rs]

    for m in messages:
        send_email(m, http)


def get_message(advertisee, advertiser, msg=None):

    pocs = db.get(advertiser.pocs)
    names = _format_names([poc.name for poc in pocs])
    emails = ', '.join([poc.email for poc in pocs])

    if msg is None:
        msg = advertisee.email

    msg = msg.format(REP=names, COMPANY=advertiser.name)

    message = MIMEText(msg)
    message['to'] = emails
    message['subject'] = 'Stop advertising on %s' % advertisee.name
    message = {'raw': base64.urlsafe_b64encode(message.as_string())}

    return message


def _format_names(names):

    if not isinstance(names, str):

        n_names = len(names)

        if n_names == 0:
            names = 'Advertiser'
        elif n_names == 1:
            names = names[0]
        elif n_names == 2:
            names = names[0] + ' and ' + names[1]
        else:
            names_tmp = ', '.join(names[:-1])
            names = names_tmp + ', and ' + names[-1]

    return names


def send_email(message, http, user_id='me'):

    gmail_service.users().messages().send(userId=user_id, body=message).execute(http=http)

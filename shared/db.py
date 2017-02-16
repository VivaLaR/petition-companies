import logging

from google.appengine.ext import ndb

import models

logger = logging.getLogger(__name__)


def get_advertisers(keys=None):

    if keys is None:
        advertisers = list(models.Advertiser.query())
    else:
        if isinstance(keys, ndb.Key):
            advertisers = keys.get()
        else:
            advertisers = ndb.get_multi(keys)

    return advertisers


def create_blank_advertisee():

    advertisee = models.Advertisee()

    return advertisee


def create_blank_advertiser():

    advertisee = models.Advertiser()

    return advertisee


def get_advertisees():

    advertisers = list(models.Advertisee.query())

    return advertisers


def get_advertisee(id_):

    a = models.Advertisee.get_by_id(id_)

    return a


def get_advertiser(id_):

    a = models.Advertiser.get_by_id(id_)

    return a


def get_poc(id_):

    print(len(id_))
    poc = models.POC.get_by_id(id_)

    return poc


def create_poc():

    poc = models.POC()

    return poc


def put(models):

    if isinstance(models, ndb.Model):
        return models.put()
    else:
        return ndb.put_multi(models)


def get(specifiers, kind=None):

    if not isinstance(specifiers, (tuple, list)):
        if kind:
            specifiers = ndb.Key(kind, specifiers)
        return specifiers.get()

    if kind:
        specifiers = [ndb.Key(kind, x) for x in specifiers]

    return ndb.get_multi(specifiers)


def delete(specifiers, kind=None):

    if not isinstance(specifiers, (tuple, list)):
        specifiers = [specifiers]

    if kind:
        specifiers = [ndb.Key(kind, x) for x in specifiers]

    ndb.delete_multi(specifiers)


def remove_advertiser(advertisee_id, advertiser_id):

    a = get_advertisee(advertisee_id)

    k = ndb.Key(models.Advertiser, advertiser_id)

    a.advertisers.remove(k)

    a.put()


def add_advertiser(advertisee_id, advertiser_id):

    a = get_advertisee(advertisee_id)

    k = ndb.Key(models.Advertiser, advertiser_id)

    a.advertisers.append(k)

    a.put()


def delete_advertisee(id_):

    if id_ is not None:
        ndb.Key(models.Advertisee, id_).delete()


def delete_advertiser(id_):

    if id_ is not None:
        advertiser = get_advertiser(id_)
        to_delete = advertiser.pocs
        to_delete.append(advertiser.key)
        ndb.delete_multi(to_delete)

        to_put = []
        for advertisee in get_advertisees():
            try:
                advertisee.advertisers.remove(advertiser.key)
            except ValueError:
                pass
            else:
                to_put.append(advertisee)

        ndb.put_multi(to_put)


def insert_advertisexs():

    email_template_breitbart = """
    Hey %s,

    I'm getting in touch with you as part of the Sleeping Giants campaign. Did you know that %s has ads appearing on Breitbart.com?
    Breitbart is widely known as a hate speech site, regularly distributing anti-Semitic, anti-Muslim, xenophobic and misogynist propaganda - and it's being propped up by ad revenues sent from companies like yours via 3rd party ad platforms.

    Is this something you support?

    If not, you can change this by contacting your ad agency and asking them to exclude Breitbart from your media buy.
    Will you please consider joining 700+ companies who have already blacklisted Breitbart? Please let me know. We would love to add you to the confirmed list!

    I hope to see the advertisements taken down,
    Sal
    """

    breitbart_key = models.Advertisee(name='Breitbart', description='Hateful website with neonazi leader.', email=email_template_breitbart).put()
    poc_kayak_key = models.POC(name='Stephanie', email='sretcho@kayak.com').put()
    kayak_key = models.Advertiser(name='Kayak', pocs=[poc_kayak_key]).put()
    breitbart = breitbart_key.get()
    breitbart.advertisers.append(kayak_key)
    breitbart.put()


def insert_advertiser():

    poc_uber_key = models.POC(name='Alex', email='alex@gmail.com').put()
    models.Advertiser(name='Uber', pocs=[poc_uber_key]).put()

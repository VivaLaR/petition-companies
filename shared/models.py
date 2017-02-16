from google.appengine.ext import ndb


class Advertiser(ndb.Model):

    name = ndb.StringProperty('n')
    pocs = ndb.KeyProperty('p', kind='POC', repeated=True)


class Advertisee(ndb.Model):

    name = ndb.StringProperty('n')
    advertisers = ndb.KeyProperty('a', kind='Advertiser', repeated=True)
    description = ndb.StringProperty('d')
    email = ndb.StringProperty('e')


class POC(ndb.Model):

    name = ndb.StringProperty('n')
    email = ndb.StringProperty('e', required=True)


class UserPreference(ndb.Model):

    advertiser = ndb.KeyProperty(kind='Advertiser')
    advertisee = ndb.KeyProperty(kind='Advertisee')


class AdvertiseeDefaultMessage(ndb.Model):

    advertisee = ndb.KeyProperty(kind='Advertisee')
    message_ = ndb.StringProperty(default=None)
    message = ndb.ComputedProperty(lambda self: self.message_ or self.advertisee.get().email)


class User(ndb.Model):

    email = ndb.StringProperty('e')
    user_a_checks = ndb.KeyProperty(UserPreference, repeated=True)
    advertisee_descriptions = ndb.StructuredProperty(AdvertiseeDefaultMessage, repeated=True)


if __name__ == '__main__':

    subject_template_breitbart = "%s Advertising on Breitbart"

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

    poc_kayak_key = POC(name='Stephanie', email='sretcho@kayak.com').put()
    Advertiser('Kayak', [poc_kayak_key]).put()

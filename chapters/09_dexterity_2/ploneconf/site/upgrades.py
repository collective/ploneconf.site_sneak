from plone import api
import logging

default_profile = 'profile-ploneconf.site:default'

logger = logging.getLogger('ploneconf.site')


def upgrade_site(setup):
    setup.runImportStepFromProfile(default_profile, 'typeinfo')
    catalog = api.portal.get_tool('portal_catalog')
    portal = api.portal.get()
    if 'the-event' not in portal:
        theevent = api.content.create(
            container=portal,
            type='Folder',
            id='the-event',
            title='The event')
    else:
        theevent = portal['the-event']
    if 'talks' not in theevent:
        talks = api.content.create(
            container=theevent,
            type='Folder',
            id='talks',
            title='Talks')
    else:
        talks = theevent['talks']
    talks_url = talks.absolute_url()
    brains = catalog(portal_type='talk')
    for brain in brains:
        if talks_url in brain.getURL():
            continue
        obj = brain.getObject()
        logger.info('Moving %s to %s' % (obj.absolute_url(), talks.absolute_url()))
        api.content.move(
            source=obj,
            target=talks,
            safe_id=True)

from plone import api
import logging

default_profile = 'profile-ploneconf.site:default'

logger = logging.getLogger('ploneconf.site')


def upgrade_site(self):
    self.runImportStepFromProfile(default_profile, 'typeinfo')
    catalog = api.portal.get_tool('portal_catalog')
    portal = api.portal.get()
    if 'talks' not in portal:
        talks = api.content.create(
            container=portal,
            type='Folder',
            id='talks',
            title='Talks')
    else:
        talks = portal['talks']
    talks_url = talks.absolute_url()
    brains = catalog(portal_type='talk')
    for brain in brains:
        if talks_url in brain.getURL():
            continue
        obj = brain.getObject()
        logger.info('Moving %s' % obj.absolute_url())
        api.content.move(
            source=obj,
            target=talks,
            safe_id=True)

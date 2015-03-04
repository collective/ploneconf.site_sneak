# -*- coding: utf-8 -*-
from plone import api
import logging

default_profile = 'profile-ploneconf.site:default'
logger = logging.getLogger('ploneconf.site')


def upgrade_site(setup):
    setup.runImportStepFromProfile(default_profile, 'typeinfo')
    catalog = api.portal.get_tool('portal_catalog')
    portal = api.portal.get()
    # Create a folder 'The event' if needed
    if 'the-event' not in portal:
        theevent = api.content.create(
            container=portal,
            type='Folder',
            id='the-event',
            title='The event')
    else:
        theevent = portal['the-event']

    # Create folder 'Talks' inside 'The event' if needed
    if 'talks' not in theevent:
        talks = api.content.create(
            container=theevent,
            type='Folder',
            id='talks',
            title='Talks')
    else:
        talks = theevent['talks']
    talks_url = talks.absolute_url()

    # Get all talks
    brains = catalog(portal_type='talk')
    for brain in brains:
        if talks_url in brain.getURL():
            # Skip if the talk is already in target-folder
            continue
        obj = brain.getObject()
        logger.info(
            'Moving %s to %s' % (obj.absolute_url(), talks.absolute_url()))
        # Move each talk to the folder '/the-event/talks'
        api.content.move(
            source=obj,
            target=talks,
            safe_id=True)

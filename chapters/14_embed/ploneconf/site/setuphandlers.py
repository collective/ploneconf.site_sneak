# -*- coding: UTF-8 -*-
from plone.app.controlpanel.security import ISecuritySchema
from plone import api
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.app.dexterity.behaviors import constrains

import logging

PROFILE_ID = 'profile-ploneconf.site:default'
logger = logging.getLogger('ploneconf.site')


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('ploneconf.site_various.txt') is None:
        return

    site = api.portal.get()
    set_up_security(site)
    set_up_content(site)


def set_up_security(site):
    secSchema = ISecuritySchema(site)
    secSchema.set_enable_self_reg(True)


def set_up_content(site):
    """Create and configure some initial content"""
    if 'talks' in site:
        return
    talks = api.content.create(
        container=site,
        type='Folder',
        id='talks',
        title='Talks')
    api.content.transition(talks, 'publish')
    api.group.grant_roles(
        groupname='AuthenticatedUsers',
        roles=['Contributor'],
        obj=talks)
    # Enable constraining
    behavior = ISelectableConstrainTypes(talks)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(['talk'])
    behavior.setImmediatelyAddableTypes(['talk'])
    logger.info("Created and configured %s" % talks.absolute_url())

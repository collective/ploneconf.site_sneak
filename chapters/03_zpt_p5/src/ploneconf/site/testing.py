# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig

import ploneconf.site


class PloneconfSiteLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file(
            'configure.zcml',
            ploneconf.site,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ploneconf.site:default')


PLONECONF_SITE_FIXTURE = PloneconfSiteLayer()


PLONECONF_SITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONECONF_SITE_FIXTURE,),
    name='PloneconfSiteLayer:IntegrationTesting'
)


PLONECONF_SITE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONECONF_SITE_FIXTURE,),
    name='PloneconfSiteLayer:FunctionalTesting'
)


PLONECONF_SITE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONECONF_SITE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='PloneconfSiteLayer:AcceptanceTesting'
)

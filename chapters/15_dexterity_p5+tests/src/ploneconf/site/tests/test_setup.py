# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""
from ploneconf.site.testing import PLONECONF_SITE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestInstall(unittest.TestCase):
    """Test installation of ploneconf.site into Plone."""

    layer = PLONECONF_SITE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ploneconf.site is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('ploneconf.site'))

    def test_uninstall(self):
        """Test if ploneconf.site is cleanly uninstalled."""
        self.installer.uninstallProducts(['ploneconf.site'])
        self.assertFalse(self.installer.isProductInstalled('ploneconf.site'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IPloneconfSiteLayer is registered."""
        from ploneconf.site.interfaces import IPloneconfSiteLayer
        from plone.browserlayer import utils
        self.assertIn(IPloneconfSiteLayer, utils.registered_layers())

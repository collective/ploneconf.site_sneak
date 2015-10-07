# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from ploneconf.site.testing import PLONECONF_SITE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that ploneconf.site is properly installed."""

    layer = PLONECONF_SITE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ploneconf.site is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('ploneconf.site'))

    def test_browserlayer(self):
        """Test that IPloneconfSiteLayer is registered."""
        from ploneconf.site.interfaces import IPloneconfSiteLayer
        from plone.browserlayer import utils
        self.assertIn(IPloneconfSiteLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PLONECONF_SITE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['ploneconf.site'])

    def test_product_uninstalled(self):
        """Test if ploneconf.site is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('ploneconf.site'))

    def test_browserlayer_removed(self):
        """Test that IPloneconfSiteLayer is removed."""
        from ploneconf.site.interfaces import IPloneconfSiteLayer
        from plone.browserlayer import utils
        self.assertNotIn(IPloneconfSiteLayer, utils.registered_layers())

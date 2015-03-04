# -*- coding: UTF-8 -*-
from Products.Five.browser import BrowserView
from plone.dexterity.browser.view import DefaultView
from plone import api

import logging
logger = logging.getLogger(__name__)


class DemoView(BrowserView):
    """This is a sample browser view with one method."""

    def get_types(self):
        """Returns a dict with type names and the amount of items
        for this type in the site.
        """
        portal_catalog = api.portal.get_tool('portal_catalog')
        portal_types = api.portal.get_tool('portal_types')
        content_types = portal_types.listContentTypes()
        results = []
        for ct in content_types:
            brains = portal_catalog(portal_type=ct)
            if brains:
                results.append({
                    'type': ct,
                    'qtt': len(brains),
                })
            else:
                logger.info("No elements of type {0}".format(ct))

        return results


class TalkView(DefaultView):
    """The default view for talks"""


class TalkListView(BrowserView):
    """ A list of talks
    """

    def talks(self):
        results = []
        portal_catalog = api.portal.get_tool('portal_catalog')
        current_path = "/".join(self.context.getPhysicalPath())

        brains = portal_catalog(portal_type="talk",
                                path=current_path)
        for brain in brains:
            results.append({
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                'audience': ', '.join(brain.audience or []),
                'type_of_talk': brain.type_of_talk,
                'speaker': brain.speaker,
                'uuid': brain.UID,
                })
        return results

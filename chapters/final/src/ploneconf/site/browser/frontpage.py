# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView

import datetime


class FrontPageView(BrowserView):
    """The view the conference frontpage
    """

    def talks(self):
        """Get todays talks"""
        results = []
        catalog = api.portal.get_tool('portal_catalog')
        today = datetime.date.today()
        brains = catalog(
            portal_type='talk',
            sort_on='start',
            sort_order='descending'
        )
        for brain in brains:
            if brain.start.date() == today:
                results.append({
                    'title': brain.Title,
                    'description': brain.Description,
                    'url': brain.getURL(),
                    'audience': ', '.join(brain.audience or []),
                    'type_of_talk': brain.type_of_talk,
                    'speaker': brain.speaker,
                    'uuid': brain.UID,
                    'start': brain.start,
                    'room': brain.room,
                    })
        return results

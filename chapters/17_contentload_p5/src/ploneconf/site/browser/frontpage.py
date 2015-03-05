# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api

import datetime


class FrontPageView(BrowserView):
    """The view the conference frontpage
    """

    def talks(self):
        """Get todays talks"""
        results = []
        catalog = api.portal.get_tool('portal_catalog')
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        date_range_query = {'query': (today, tomorrow), 'range': 'min:max'}
        brains = catalog(
            portal_type='talk',
            start=date_range_query,
            sort_on='start',
            sort_order='ascending'
        )
        for brain in brains:
                speaker = self.speaker(brain)
                results.append({
                    'title': brain.Title,
                    'description': brain.Description,
                    'url': brain.getURL(),
                    'audience': ', '.join(brain.audience or []),
                    'type_of_talk': brain.type_of_talk,
                    'speaker': speaker.title if speaker else None,
                    'uuid': brain.UID,
                    'start': brain.start,
                    'room': brain.room,
                    })
        return results

    def speaker(self, brain):
        """Return the speaker for a talk"""
        talk = brain.getObject()
        relation = talk.speaker_rel
        if not relation:
            return
        obj = relation.to_object
        if api.user.has_permission('View', obj=obj):
            return obj

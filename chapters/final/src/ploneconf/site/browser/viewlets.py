# -*- coding: utf-8 -*-
from collections import OrderedDict
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram
from ploneconf.site.behaviors.social import ISocial
from ploneconf.site.content.sponsor import LevelVocabulary
from random import shuffle
from time import time


class SocialViewlet(ViewletBase):

    def lanyrd_link(self):
        adapted = ISocial(self.context)
        return adapted.lanyrd


class SponsorsViewlet(ViewletBase):

    @ram.cache(lambda *args: time() // (60 * 60))  # cache for 1 hour
    def _sponsors(self):
        """Return a list of dicts with info from sponsors.
        """
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='sponsor')
        results = []
        for brain in brains:
            obj = brain.getObject()
            # Get the view '@@images'
            scales = api.content.get_view(
                name='images',
                context=obj,
                request=self.request)
            # Scale the logo to a fixed size
            scale = scales.scale(
                'logo',
                width=200,
                height=80,
                direction='down')
            # Create the complete img-tag from the the scale-object
            tag = scale.tag() if scale else ''
            if not tag:
                # only display sponsors with a logo
                continue
            # Create a dict with the necessary info
            results.append(dict(
                title=brain.Title,
                description=brain.Description,
                tag=tag,
                url=obj.url or obj.absolute_url(),
                level=obj.level
            ))
        return results

    def sponsors(self):
        # Get the list of dicts from the method above
        sponsors = self._sponsors()
        if not sponsors:
            return
        # Make sure the results are ordered
        results = OrderedDict()
        # Get all sponsoring-levels in the right order
        levels = [i.value for i in LevelVocabulary]
        for level in levels:
            level_sponsors = []
            # Add sponsors to a list level_sponsors if the level is right
            for sponsor in sponsors:
                if level == sponsor['level']:
                    level_sponsors.append(sponsor)
            if not level_sponsors:
                continue
            # Randomly order the sponsors in level_sponsors
            shuffle(level_sponsors)
            # {'gold': [sponsor, ...], ...} where sponsor is a dict
            results[level] = level_sponsors
        return results
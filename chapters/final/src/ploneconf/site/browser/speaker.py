# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.browser.view import DefaultView
from z3c.relationfield.index import dump
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
import logging

logger = logging.getLogger(__name__)


class SpeakerView(DefaultView):
    """The default view for talks"""


    def talks(self):
        """Get talks from backrelations"""
        retval = []
        cat = getUtility(ICatalog)
        int_id = dump(self.context, cat, {})
        if not int_id:
            return []
        relations = cat.findRelations(dict(to_id=int_id))
        for relation in relations:
            if relation.isBroken():
                retval.append(dict(href='',
                                   title='broken reference'))
            else:
                obj = relation.from_object
                retval.append(dict(href=obj.absolute_url(),
                                   title=obj.title))
        return retval

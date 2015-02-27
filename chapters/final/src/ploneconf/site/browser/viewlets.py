# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import ViewletBase
from ploneconf.site.behaviors.social import ISocial
from datetime import datetime

CONFERENCE_START_DATE = datetime(2015, 10, 12)


class SocialViewlet(ViewletBase):

    def lanyrd_link(self):
        adapted = ISocial(self.context)
        return adapted.lanyrd


class DaysToConferenceViewlet(ViewletBase):

    def date(self):
        return CONFERENCE_START_DATE

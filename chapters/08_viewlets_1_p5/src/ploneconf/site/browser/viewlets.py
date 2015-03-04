# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import ViewletBase
from ploneconf.site.behaviors.social import ISocial


class SocialViewlet(ViewletBase):

    def lanyrd_link(self):
        adapted = ISocial(self.context)
        return adapted.lanyrd

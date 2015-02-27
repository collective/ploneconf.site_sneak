# -*- coding: utf-8 -*-
from plone.dexterity.browser.view import DefaultView
from plone import api

import logging
logger = logging.getLogger(__name__)


class SpeakerView(DefaultView):
    """The default view for talks"""


    def talks(self):
        """Get talks from backrelations"""
        return []

# -*- coding: utf-8 -*-
from plone.dexterity.browser.view import DefaultView
import logging

logger = logging.getLogger(__name__)


class SpeakerView(DefaultView):
    """The default view for talks"""

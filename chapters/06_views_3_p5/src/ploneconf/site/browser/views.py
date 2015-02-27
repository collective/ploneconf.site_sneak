# -*- coding: UTF-8 -*-
from Products.Five.browser import BrowserView
from plone import api
from plone.dexterity.browser.view import DefaultView

import logging
logger = logging.getLogger(__name__)


class DemoView(BrowserView):
    """ This is a sample browser view with one method.
    """

class TalkView(DefaultView):
    """ The default view for talks
    """


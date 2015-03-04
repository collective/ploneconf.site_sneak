# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IPloneconfSiteLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ITalk(Interface):
    """Marker interface for Talks"""

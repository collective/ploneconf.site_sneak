# -*- coding: utf-8 -*-
from plone.supermodel import model, directives
from plone.autoform.interfaces import IFormFieldProvider
from zope import schema
from zope.interface import alsoProvides
from plone.autoform.interfaces import IFormFieldProvider


class ISocial(model.Schema):

    directives.fieldset(
        'social',
        label=u'Social',
        fields=('lanyrd',),
    )

    lanyrd = schema.URI(
        title=u"Lanyrd-link",
        description=u"Add URL",
        required=False,
    )

alsoProvides(ISocial, IFormFieldProvider)

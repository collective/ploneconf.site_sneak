# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.namedfile import field as namedfile
from plone.supermodel.directives import fieldset
from plone.supermodel import model
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from ploneconf.site import MessageFactory as _


LevelVocabulary = SimpleVocabulary(
    [SimpleTerm(value=u'platinum', title=u'Platinum Sponsor'),
     SimpleTerm(value=u'gold', title=u'Gold Sponsor'),
     SimpleTerm(value=u'silver', title=u'Silver Sponsor'),
     SimpleTerm(value=u'bronze', title=u'Bronze Sponsor')]
    )


class ISponsor(model.Schema):
    """Dexterity-Schema for Sponsors
    """

    directives.widget(level=RadioFieldWidget)
    level = schema.Choice(
        title=u"Sponsoring Level",
        vocabulary=LevelVocabulary,
        required=True
    )

    text = RichText(
        title=u"Text",
        required=False
    )

    url = schema.URI(
        title=u"Link",
        required=False
    )

    fieldset('Images', fields=['logo', 'advertisment'])
    logo = namedfile.NamedBlobImage(
        title=u"Logo",
        required=False,
    )

    advertisment = namedfile.NamedBlobImage(
        title=u"Advertisment (Gold-sponsors and above)",
        required=False,
    )

    directives.read_permission(notes="cmf.ManagePortal")
    directives.write_permission(notes="cmf.ManagePortal")
    notes = RichText(
        title=u"Secret Notes (only for site-admins)",
        required=False
    )

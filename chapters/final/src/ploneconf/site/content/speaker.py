# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.namedfile import field as namedfile
from plone.supermodel import model
from ploneconf.site import _
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class ISpeaker(model.Schema):
    """Dexterity-Schema for Speaker
    """

    title = schema.TextLine(
        title=_(u'Name'),
        required=True,
    )

    email = schema.TextLine(
        title=_(u'E-Mail'),
        required=False,
    )

    homepage = schema.URI(
        title=_(u'Homepage'),
        required=False,
    )

    biography = RichText(
        title=_(u'Biography'),
        required=False,
    )

    company = schema.TextLine(
        title=_(u'Company'),
        required=False,
    )

    twitter_name = schema.TextLine(
        title=_(u'Twitter-Name'),
        required=False,
    )

    irc_name = schema.TextLine(
        title=_(u'IRC-Name'),
        required=False,
    )

    image = namedfile.NamedBlobImage(
        title=_(u'Image'),
        required=False,
    )

    talks = RelationList(
        title=_(u'Talks by this speaker'),
        value_type=RelationChoice(
            title=_(u'Talks'),
            source=CatalogSource(portal_type='talk')),
        required=False,
    )

# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone import api
from plone.app.dexterity.behaviors import constrains
from logging import getLogger

logger = getLogger(__name__)


STRUCTURE = [
    {
        'type': 'Document',
        'title': u'Plone Conference 2022',
        'id': 'plone-conference-2022',
        'description': u'',
    },
    {
        'type': 'Folder',
        'title': u'The Event',
        'id': 'the-event',
        'description': u'Plone Conference 2022',
        'default-page': 'frontpage-for-the-event',
        'children': [{
            'type': 'Document',
            'title': u'Frontpage for the-event',
            'id': 'frontpage-for-the-event',
            'description': u'',
            },
            {
            'type': 'Folder',
            'title': u'Talks',
            'id': 'talks',
            'description': u'',
            'layout': 'talklistview',
            },
            {
            'type': 'Folder',
            'title': u'Training',
            'id': 'training',
            'description': u'',
            },
            {
            'type': 'Folder',
            'title': u'Sprint',
            'id': 'sprint',
            'description': u'',
            },
        ]
    },
    {
        'type': 'Folder',
        'title': u'Talks',
        'id': 'talks',
        'description': u'Submit your talks here!',
        'layout': '@@talklistview',
        'allowed_types': ['talk'],
        'local_roles': [{
            'group': 'AuthenticatedUsers',
            'roles': ['Contributor']
        }],
    },
    {
        'type': 'Folder',
        'title': u'News',
        'id': 'news',
        'description': u'News about the Plone Conference',
        'children': [{
            'type': 'News Item',
            'title': u'Submit your talks!',
            'id': 'submit-your-talks',
            'description': u'',}
        ],
    },
    {
        'type': 'Folder',
        'title': u'Events',
        'id': 'events',
        'description': u'Dates to keep in mind',
    },
]

def isNotCurrentProfile(context):
    return context.readDataFile('ploneconfsite_marker.txt') is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return
    # Do something during the installation of this package


def content(context):
    if context.readDataFile('ploneconfsite_content_marker.txt') is None:
        return
    portal = api.portal.get()
    for item in STRUCTURE:
        _create_content(item, portal)


def _create_content(item, container):
    new = container.get(item['id'], None)
    if not new:
        new = api.content.create(
            type=item['type'],
            container=container,
            title=item['title'],
            id=item['id'],
            safe_id=False)
        logger.info('Created item {}'.format(new.absolute_url()))
    if item.get('layout', False):
        new.setLayout(item['layout'])
    if item.get('default-page', False):
        new.setDefaultPage(item['default-page'])
    if item.get('allowed_types', False):
        _constrain(new, item['allowed_types'])
    if item.get('local_roles', False):
        for local_role in item['local_roles']:
            api.group.grant_roles(
                groupname=local_role['group'],
                roles=local_role['roles'],
                obj=new)
    api.content.transition(new, to_state=item.get('state', 'published'))
    new.reindexObject()
    # call recursively for children
    for subitem in item.get('children', []):
        _create_content(subitem, new)


def _constrain(context, allowed_types):
    behavior = ISelectableConstrainTypes(context)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(allowed_types)
    behavior.setImmediatelyAddableTypes(allowed_types)

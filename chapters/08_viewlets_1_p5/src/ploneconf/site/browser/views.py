from Products.Five.browser import BrowserView
from plone import api
from plone.dexterity.browser.view import DefaultView


class DemoView(BrowserView):
    """ This does nothing so far
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        # Implement your own actions

        # This renders the template that was registered in zcml like this:
        #   template="templates/training.pt"
        return super(DemoView, self).__call__()
        # If you don't register a template in zcml the Superclass of
        # DemoView will have no __call__-method!
        # In that case you have to call the template like this:
        # from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
        # class DemoView(BrowserView):
        # template = ViewPageTemplateFile('templates/training.pt')
        # def __call__(self):
        #    return self.template()


class TalkView(DefaultView):
    """ The default view for talks
    """


class TalkListView(BrowserView):
    """ A list of talks
    """

    def talks(self):
        results = []
        portal_catalog = api.portal.get_tool('portal_catalog')
        current_path = "/".join(self.context.getPhysicalPath())

        brains = portal_catalog(portal_type="talk",
                                path=current_path)
        for brain in brains:
            talk = brain.getObject()
            results.append({
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                'audience': ', '.join(talk.audience),
                'type_of_talk': talk.type_of_talk,
                'speaker': talk.speaker,
                'uuid': brain.UID,
                })
        return results

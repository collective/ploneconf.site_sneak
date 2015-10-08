from Products.Five.browser import BrowserView
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

from pkg_resources import resource_stream
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone.testing.z2 import Browser
from ploneconf.site.testing import PLONECONF_SITE_FUNCTIONAL_TESTING
from ploneconf.site.testing import PLONECONF_SITE_INTEGRATION_TESTING
from zope.component import createObject
from zope.component import queryUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
import unittest


class TalkIntegrationTest(unittest.TestCase):

    layer = PLONECONF_SITE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='talk')
        self.assertTrue(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='talk')
        schema = fti.lookupSchema()
        self.assertTrue(schema)
        # self.assertEqual(ITalk, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='talk')
        factory = fti.factory
        talk = createObject(factory)
        # self.assertTrue(ITalk.providedBy(talk))
        self.assertTrue(talk)

    def test_adding(self):
        self.portal.invokeFactory('talk', 'talk')
        self.assertTrue(self.portal.talk)
        # self.assertTrue(ITalk.providedBy(self.portal.talk))

    def test_talklistempty(self):
        view = api.content.get_view(name='talklistview',
                                    context=self.portal,
                                    request=self.request)
        talks = view.talks()
        self.assertEquals([], talks)

    def test_talklist(self):
        view = api.content.get_view(name='talklistview',
                                    context=self.portal,
                                    request=self.request)
        api.content.create(container=self.portal,
                           type='talk',
                           id='talk',
                           title='A Talk')
        talks = view.talks()
        self.assertEquals(1, len(talks))
        self.assertEquals(['start',
                           'audience',
                           'speaker',
                           'description',
                           'title',
                           'url',
                           'type_of_talk',
                           'room',
                           'uuid'],
                          talks[0].keys())

    def test_talklist_multipleaudiences(self):
        view = api.content.get_view(name='talklistview',
                                    context=self.portal,
                                    request=self.request)
        api.content.create(container=self.portal,
                           type='talk',
                           id='talk',
                           title='A Talk')
        self.portal.talk.audience = ['alpha', 'beta']
        notify(ObjectModifiedEvent(self.portal.talk))
        talks = view.talks()
        self.assertEquals(1, len(talks))
        self.assertEquals('alpha, beta', talks[0]['audience'])

    def test_talklist_filtering(self):
        api.content.create(container=self.portal,
                           type='talk',
                           id='talk',
                           title='A Talk')
        api.content.create(container=self.portal,
                           type='Folder',
                           id='talks-folder',
                           title='A talks Folder')
        api.content.create(container=self.portal['talks-folder'],
                           type='talk',
                           id='talk',
                           title='A Talk')
        api.content.create(container=self.portal['talks-folder'],
                           type='Document',
                           id='a Document',
                           title='A Document')
        view = api.content.get_view(name='talklistview',
                                    context=self.portal['talks-folder'],
                                    request=self.request)
        talks = view.talks()
        self.assertEquals(1, len(talks))
        self.assertEquals('A Talk', talks[0]['title'])


class SlowTalkIntegrationTest(unittest.TestCase):

    layer = PLONECONF_SITE_INTEGRATION_TESTING

    level = 2

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_talklist_many_results(self):
        view = api.content.get_view(name='talklistview',
                                    context=self.portal,
                                    request=self.request)
        for i in range(101):
            api.content.create(container=self.portal,
                               type='talk',
                               id='talk_{}'.format(i),
                               title='Talk {}'.format(i))
        talks = view.talks()
        self.assertEquals(101, len(talks))
        self.assertTrue(16, len(talks[-1]['uuid']))


class TalkFunctionalTest(unittest.TestCase):

    layer = PLONECONF_SITE_FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()

        # Set up browser
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_add_task(self):
        self.browser.open(self.portal_url + '/++add++talk')
        ctrl = self.browser.getControl
        ctrl(name="form.widgets.IDublinCore.title").value = "My Talk"
        ctrl(name="form.widgets.IDublinCore.description").value = \
            "This is my talk"
        ctrl(name="form.widgets.type_of_talk").value = ["Talk"]
        ctrl(name="form.widgets.details").value = "Long awesome talk"
        ctrl(name="form.widgets.audience:list").value = ["Advanced"]
        ctrl(name="form.widgets.speaker").value = "Team Banzai"
        ctrl(name="form.widgets.email").value = "banzai@example.com"
        img_ctrl = ctrl(name="form.widgets.image")
        img_ctrl.add_file(resource_stream(__name__, 'plone.png'),
                          'image/png', 'plone.png')
        ctrl(name="form.widgets.speaker_biography").value = \
            "Team Banzai is awesome, we are on Wikipedia!"
        ctrl("Save").click()

        talk = self.portal['my-talk']

        self.assertEqual('My Talk', talk.title)
        self.assertEqual('This is my talk', talk.description)
        self.assertEqual('Talk', talk.type_of_talk)
        self.assertEqual('Long awesome talk', talk.details.output)
        self.assertEqual({'Advanced'}, talk.audience)
        self.assertEqual('Team Banzai', talk.speaker)
        self.assertEqual((491, 128), talk.image.getImageSize())
        self.assertEqual('Team Banzai is awesome, we are on Wikipedia!',
                         talk.speaker_biography.output)

    def test_view_task(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            "talk",
            id="my-talk",
            title="My Talk",
        )

        import transaction
        transaction.commit()

        self.browser.open(self.portal_url + '/my-talk')

        self.assertTrue('My Talk' in self.browser.contents)

    def test_custom_template(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            "talk",
            id="my-talk",
            title="My Talk",
        )

        import transaction
        transaction.commit()

        self.browser.open(self.portal_url + '/training')

        self.assertIn('Dexterity for the win', self.browser.contents)
        self.assertIn('Deco is the future', self.browser.contents)
        self.assertIn('The State of Plone', self.browser.contents)
        self.assertIn('Diazo designs are great', self.browser.contents)

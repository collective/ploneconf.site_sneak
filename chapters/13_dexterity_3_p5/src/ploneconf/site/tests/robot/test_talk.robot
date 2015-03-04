# ============================================================================
# EXAMPLE ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s plonetraining.testing -t test_talk.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src plonetraining.testing.testing.PLONETRAINING_TESTING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_talk.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Talk
  Given a logged-in site administrator
    and an add talk form
   When I type 'My Talk' into the title field
    and I type 'Awesome talk' into the details field
    and I type 'Team Banzai' into the speakers field
    and I type 'banzai@example.com' into the email field
    and I submit the form
   Then a talk with the title 'My Talk' has been created

Scenario: As a site administrator I can view a Talk
  Given a logged-in site administrator
    and a talk 'My Talk'
   When I go to the talk view
   Then I can see the talk title 'My Talk'

Scenario: As a visitor I can view the new talk list
   When I go to the talk list view
   Then I can see a talk about 'Diazo designs are great'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add talk form
  Go To  ${PLONE_URL}/++add++talk

a talk 'My Talk'
  Create content  type=talk  id=my-talk  title=My Talk


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I type '${details}' into the details field
  Select frame  form-widgets-details_ifr
  Input text  tinymce  ${details}
  Unselect Frame

I type '${speaker}' into the speakers field
  Input Text  name=form.widgets.speaker  ${speaker}

I type '${email}' into the email field
  Input Text  name=form.widgets.email  ${email}

I submit the form
  Click Button  Save

I go to the talk view
  Go To  ${PLONE_URL}/my-talk
  Wait until page contains  Site Map

I go to the talk list view
  Go To  ${PLONE_URL}/demoview
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a talk with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the talk title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

I can see a talk about '${topic}'
  Wait until page contains  Site Map
  Page should contain  ${topic}

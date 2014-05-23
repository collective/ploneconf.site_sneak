from plone.api.content import transition
from plone.api.content import get_state
from starzel.votable_behavior.interfaces import IVoting


def votable_update(votable_object, event):
    votable = IVoting(votable_object)
    if get_state(votable_object) == 'pending':
        if votable.average_vote() > 0.5:
            transition(votable_object, transition='publish')

from clarent import auth
from txampext.commandtests import CommandTestMixin
from twisted.trial.unittest import SynchronousTestCase


class RegisterTests(CommandTestMixin, SynchronousTestCase):
    argumentStrings = argumentObjects = [
        (b"email", b"xyzzy")
    ]
    responseStrings = responseObjects = []
    errors = dict([
        auth.NotRegistered.asAMP(),
        auth.AlreadyRegistered.asAMP(),
        auth.BadEmailAddress.asAMP()
    ])
    fatalErrors = {}
    requiresAnswer = True

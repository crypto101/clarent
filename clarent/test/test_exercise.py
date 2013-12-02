from clarent import exercise
from twisted.trial.unittest import SynchronousTestCase
from txampext.commandtests import CommandTestMixin

class SubmissionTests(SynchronousTestCase, CommandTestMixin):
    command = exercise.Submit

    argumentObjects = {
        b"step": 1,
        b"submission": b"xyzzy"
    }
    argumentStrings = {
        b"step": "1",
        b"submission": b"xyzzy"
    }

    responseObjects = {}
    responseStrings = {}

    errors = dict([
        exercise.UnknownStep.asAMP(),
        exercise.WrongStep.asAMP(),
        exercise.IncorrectSubmission.asAMP()
    ])
    fatalErrors = {}

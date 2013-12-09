from clarent import exercise
from twisted.trial.unittest import SynchronousTestCase
from txampext.commandtests import CommandTestMixin


NUL = "\x00"


class GetExercisesTests(SynchronousTestCase, CommandTestMixin):
    command = exercise.GetExercises
    argumentObjects = {
        b"solved": False
    }
    argumentStrings = {
        b"solved": "False"
    }
    responseObjects = {
        b"exercises": [
            {b"identifier": "a", b"title": u"\N{SNOWMAN}"},
            {b"identifier": "b", b"title": u"\N{CLOUD}"}
        ]
    }

    P_IDENTIFIER = "\x0a" + "identifier"
    P_TITLE = "\x05" + "title"
    P_SNOWMAN = "\x03" + u"\N{SNOWMAN}".encode("utf-8")
    P_CLOUD = "\x03" + u"\N{CLOUD}".encode("utf-8")

    responseStrings = {
        b"exercises": b"".join([
            NUL, P_IDENTIFIER, NUL, "\x01", "a",
            NUL, P_TITLE, NUL, P_SNOWMAN, NUL,
            NUL,
            NUL, P_IDENTIFIER, NUL, "\x01", "b",
            NUL, P_TITLE, NUL, P_CLOUD, NUL,
            NUL
        ])
    }
    errors = fatalErrors = {}
    requiresAnswer = True



class GetExerciseDetailsTests(SynchronousTestCase, CommandTestMixin):
    command = exercise.GetExerciseDetails
    argumentObjects = {
        b"identifier": b"a"
    }
    argumentStrings = {
        b"identifier": b"a"
    }
    responseObjects = {
        b"title": u"",
        b"description": u"",
        b"solved": True
    }
    responseStrings = {
        b"title": b"",
        b"description": b"",
        b"solved": b"True"
    }
    errors = fatalErrors = {}
    requiresAnswer = True



class NotifySolvedTests(SynchronousTestCase, CommandTestMixin):
    command = exercise.NotifySolved
    argumentObjects = {
        b"identifier": "a",
        b"title": u"\N{SNOWMAN}"
    }
    argumentStrings = {
        b"identifier": "a",
        b"title": u"\N{SNOWMAN}".encode("utf-8")
    }
    responseObjects = responseStrings = {}
    errors = fatalErrors = {}
    requiresAnswer = False

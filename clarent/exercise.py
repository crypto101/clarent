"""
Public exercise API.
"""
from twisted.protocols import amp
from txampext.errors import Error


class UnknownExercise(Error):
    """The exercise was not recognized.

    """



class GetExercises(amp.Command):
    """
    Gets the identifiers and titles of some exercises.
    """
    arguments = [
        (b"solved", amp.Boolean())
    ]
    response = [
        (b"exercises", amp.AmpList([
            (b"identifier", amp.String()),
            (b"title", amp.Unicode())
        ]))
    ]



class GetExerciseDetails(amp.Command):
    """
    Gets the details of a partiucular exercise.
    """
    arguments = [
        (b"identifier", amp.String())
    ]
    response = [
        (b"title", amp.Unicode()),
        (b"description", amp.Unicode()),
        (b"solved", amp.Boolean())
    ]
    errors = dict([
        UnknownExercise.asAMP()
    ])



class NotifySolved(amp.Command):
    """Notify the client that they have solved an exercise.

    """
    arguments = [
        (b"identifier", amp.String()),
        (b"title", amp.Unicode())
    ]
    response = []
    requiresAnswer = False

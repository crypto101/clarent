"""
Public exercise API.
"""
from twisted.protocols import amp
from txampext.errors import Error


class UnknownStep(Error):
    """
    The step for which a submission was made was not recognized.
    """



class WrongStep(Error):
    """
    The step for which a submission was made was recognized, but the
    user was not on that step of the exercise.

    This can occur when a user accidentally submits something for a
    step they had previously submitted something for.
    """



class IncorrectSubmission(Error):
    """
    The submission was understood, but incorrect.
    """



class Submit(amp.Command):
    arguments = [
        (b"step", amp.Integer()),
        (b"submission", amp.String())
    ]
    response = []
    errors = dict([
        IncorrectSubmission.asAMP(),
        UnknownStep.asAMP(),
        WrongStep.asAMP()
    ])

from twisted.protocols.amp import Command, String
from txampext.errors import AMPError


class NotRegistered(AMPError):
    """The command that was invoked is only available after registration.

    """



class AlreadyRegistered(AMPError):
    """The user attempted to register when already registered.

    """



class BadEmailAddress(AMPError):
    """The e-mail address was not recognized.

    """



class Register(Command):
    arguments = [
        (b"email", String())
    ]
    response = []
    errors = dict([
        NotRegistered.asAMP(),
        AlreadyRegistered.asAMP(),
        BadEmailAddress.asAMP()
    ])

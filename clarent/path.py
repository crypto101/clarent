"""
A place to store your stuff.
"""
from os.path import expanduser
from platform import system
from twisted.python.filepath import FilePath


thisSystem = system()


def getDataPath(_system=thisSystem, _FilePath=FilePath):
    """Gets an appropriate path for storing some local data, such as TLS
    credentials.

    If the path doesn't exist, it is created.

    """
    if _system == "Windows":
        pathName = "~/Crypto101/"
    else:
        pathName = "~/.crypto101/"

    path = _FilePath(expanduser(pathName))
    if not path.exists():
        path.makedirs()

    return path

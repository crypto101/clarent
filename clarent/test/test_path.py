from clarent import path
from os.path import expanduser
from platform import system
from twisted.trial.unittest import SynchronousTestCase


class GetDataPathTests(SynchronousTestCase):
    def test_system(self):
        """The thisSystem constant is the current return value of
        ``platform.system``.

        """
        self.assertEqual(path.thisSystem, system())


    def _assertDataPathForPlatformEquals(self, platform, pathName):
        p = path.getDataPath(platform, FakeFilePath)
        self.assertEqual(p.path, expanduser(pathName))


    def test_getDataPathOnWindows(self):
        """On Windows, the data path is "~/Crypto101/", expanded.

        """
        self._assertDataPathForPlatformEquals("Windows", "~/Crypto101/")


    def test_getDataPathOnLinux(self):
        """On Linux, the data path is "~/.crypto101/", expanded.

        """
        self._assertDataPathForPlatformEquals("Linux", "~/.crypto101/")


    def test_dataPathOnOSX(self):
        """On OS X, the data path is "~/.crypto101/", expanded.

        """
        self._assertDataPathForPlatformEquals("OS X", "~/.crypto101/")


    def test_createDirectory(self):
        """If the directory does not exist, it is created.

        """
        p = path.getDataPath(_FilePath=NonExistentFakeFilePath)
        self.assertTrue(p.exists())



class FakeFilePath(object):
    """
    A fake file path.
    """
    _exists = True

    def __init__(self, path):
        self.path = path


    def exists(self):
        return self._exists



class NonExistentFakeFilePath(FakeFilePath):
    _exists = False

    def makedirs(self):
        self._exists = True

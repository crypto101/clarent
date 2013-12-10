from clarent.certificate import makeCertificate, generateKey
from inspect import getargspec
from OpenSSL.crypto import PKey, TYPE_RSA, load_privatekey, FILETYPE_PEM
from twisted.trial.unittest import SynchronousTestCase


class FakePKey(object):
    """A fake key.

    """
    def generate_key(self, keyType, keyLength):
        self.keyType, self.keyLength = keyType, keyLength



class KeyGenerationTests(SynchronousTestCase):
    """Tests for the key generation routine.

    """
    def test_pkeyDefault(self):
        """The key generation routine uses PKey by default.

        """
        argspec = getargspec(generateKey)
        default = argspec.defaults[argspec.args.index("_PKey")]
        self.assertIdentical(default, PKey)


    def test_generateKey(self):
        """The key generation routine generates 4096-bit RSA keys.

        """
        key = generateKey(_PKey=FakePKey)
        self.assertIdentical(key.keyType, TYPE_RSA)
        self.assertEqual(key.keyLength, 4096)



# This ugly private key is in here so that we can avoid generating one
# every test run.
pemTestKey = """
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDI/k18vPhKBLVfZj8TpROrf6A0QuQZVc985FUTYW1sv/kfni2a
KbeBG1d+7X0CAZM7XTzyvtoqnuUhFvOjvUwmnqtJECDcmsNzsomdG0WdZsTq2EJx
Z1gNW/fCKarmKLXvSvck++XRPcuWsM7E0bsA8O+49s69xk8rOxTDm8G71wIDAQAB
AoGAZc7KGSDu8y8nX8c+tAityfS/hTlMqLiafLx7i3GSJ7+lxKoulyQCW1cqHpTU
+SsrFKrJsHuTrnsFvJkPmCTOaOr2rwyNPNTNlTVmCHWdCXXwveqYefvH5EUwERZm
zPNm2q7R7r7iLqFugGNvEVW09nhFzB7PZV6o3UYMUzX0aiECQQD1p93Sh38v8O/j
BnNdYYVgb760kwG9rrmjRecMAc7jvXs9PjDmmie968gzGs1NGhVhJ8aLkDoZ2SGU
d36WbA/tAkEA0XT7fM10eaQi3bU2q18G0egRPu+ILyc2r5+D5GDaHQ5Ozum90R3H
4wn15hAZ6Be95f8hHeIoIm8Y/X+N3TSaUwJBAJelpikV3i0xNlVWoRcPYa/Tq817
RsLavtyNBYGDCD3MtexrnPJuTYRPronlzMEBDhuo20dCpKtaQAGP9sRTN00CQQC6
2F4XILgMYszvdd3E1cohqaDowYh8d8CivetL6NHpJYBLt9sqFiTfdV0z050omzU9
XG/QVpRy0yQ5znVgpLIdAkAf3raH4V8YkWcvJvP5HmFOZTF+oHIxewpQfF+ebhxP
6ZLFNssSL/XpWiwQKWi2NmZP30VKC+zhUByT7y+qxg4J
-----END RSA PRIVATE KEY-----
"""
testKey = load_privatekey(FILETYPE_PEM, pemTestKey)



class CertificateTests(SynchronousTestCase):
    """Tests for generating certificates.

    """
    def test_makeCertificate(self):
        """A produced certificate has the appropriate common name and e-mail
        address, and is self-signed with the given key and SHA-512.

        """
        cert = makeCertificate(testKey, u"test@example.com")

        subj = cert.get_subject()
        self.assertEqual(subj.CN, u"Crypto 101 Client")
        self.assertEqual(subj.emailAddress, u"test@example.com")

        self.assertEqual(cert.get_issuer(), cert.get_subject())
        self.assertEqual(cert.get_signature_algorithm(),
                         "sha512WithRSAEncryption")

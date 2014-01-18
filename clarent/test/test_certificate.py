from clarent import certificate
from datetime import datetime
from inspect import getargspec
from OpenSSL import crypto, SSL
from twisted.trial.unittest import SynchronousTestCase
from twisted.python.filepath import FilePath


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
        argspec = getargspec(certificate._generateKey)
        default = argspec.defaults[argspec.args.index("_PKey")]
        self.assertIdentical(default, crypto.PKey)


    def test_generateKey(self):
        """The key generation routine generates 4096-bit RSA keys.

        """
        key = certificate._generateKey(_PKey=FakePKey)
        self.assertIdentical(key.keyType, crypto.TYPE_RSA)
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
testKey = crypto.load_privatekey(crypto.FILETYPE_PEM, pemTestKey)



class CertificateTests(SynchronousTestCase):
    """Tests for generating certificates.

    """
    def test_makeCertificate(self):
        """A produced certificate has the appropriate common name and e-mail
        address, and is self-signed with the given key and SHA-512. It
        is currently valid, is not valid before today at midnight Zulu
        time, and is valid until the same date at midnight five years
        from now.

        """
        def utcnow():
            return datetime(2000, 1, 10, 18, 12)

        cert = certificate._makeCertificate(
            testKey, u"test@example.com", _utcnow=utcnow)

        subj = cert.get_subject()
        self.assertEqual(subj.CN, u"Crypto 101 Client")
        self.assertEqual(subj.emailAddress, u"test@example.com")

        self.assertFalse(cert.has_expired())
        self.assertEqual(cert.get_notBefore(), "20000110000000Z")
        self.assertEqual(cert.get_notAfter(), "20050110000000Z")

        self.assertEqual(cert.get_issuer(), cert.get_subject())
        self.assertEqual(cert.get_signature_algorithm(),
                         "sha512WithRSAEncryption")


    def test_certificateRoundtrip(self):
        """A certificate can be dumped to a string and read again.

        """
        cert = certificate._makeCertificate(testKey, u"test@example.com")
        data = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
        crypto.load_certificate(crypto.FILETYPE_PEM, data)



class MakeCredentialsTests(SynchronousTestCase):
    def setUp(self):
        self.path = FilePath(self.mktemp())
        self.path.makedirs()
        self.patch(certificate, "_generateKey", lambda: testKey)


    def _makeCredentials(self):
        return certificate.makeCredentials(self.path, u"test@example.test")


    def test_makeCredentials(self):
        """Making credentials creates a key with matching certificate and
        writes it to disk under the given path.

        """
        self.assertRaises(IOError, certificate.getContextFactory, self.path)
        self._makeCredentials()
        certificate.getContextFactory(self.path)


    def test_makeCredentialsMultipleTimes(self):
        """Attempting to generate credentials when the credentials file
        exists already raises OSError.

        """
        self.assertRaises(IOError, certificate.getContextFactory, self.path)

        self._makeCredentials()
        certificate.getContextFactory(self.path)

        self.assertRaises(OSError, self._makeCredentials)
        certificate.getContextFactory(self.path)



class SecureCiphersContextFactoryTests(SynchronousTestCase):
    def setUp(self):
        ctxFactory = FakeContextFactory()
        self.contextFactory = certificate.SecureCiphersContextFactory(ctxFactory)


    def test_noSSLv23(self):
        """SSLv2 and SSLv3 ciphersuites are disabled.

        """
        ctx = self.contextFactory.getContext()
        self.assertTrue(ctx.options & SSL.OP_NO_SSLv2)
        self.assertTrue(ctx.options & SSL.OP_NO_SSLv3)


    def test_ciphersuites(self):
        """The context factory uses the secure cipher list.

        """
        ctx = self.contextFactory.getContext()
        self.assertEqual(ctx.ciphers, certificate.ciphersuites)



class FakeContextFactory(object):
    def getContext(self):
        return FakeContext()



class FakeContext(object):
    def __init__(self):
        self.options = 0
        self.ciphers = None


    def set_options(self, opts):
        self.options |= opts


    def set_cipher_list(self, ciphers):
        self.ciphers = ciphers



class CiphersuiteTests(SynchronousTestCase):
    """Tests for the secure ciphersuites.

    """
    suites = tuple(certificate.ciphersuites.split(":"))

    def test_onlyPerfectForwardSecurity(self):
        """All suites are either DHE or ECDHE.
        """
        for suite in self.suites:
            self.assertTrue(suite.startswith("DHE") or suite.startswith("ECDHE"))


    def indicesForPrefix(self, prefix):
        """Gets all the indices of suites that start with the given prefix.

        """
        for i, suite in enumerate(self.suites):
            if suite.startswith(prefix):
                yield i


    def test_preferECDHE(self):
        """All ECDHE suites come before all DHE suites.

        """

        lastECDHE = max(self.indicesForPrefix("ECDHE-"))
        firstDHE = min(self.indicesForPrefix("DHE-"))
        self.assertGreater(firstDHE, lastECDHE)


    def assertPreferred(self, preferred, notPreferred):
        """Asserts that one suite is preferred over another.

        """
        preferredIndex = self.suites.index(preferred)
        notPreferredIndex = self.suites.index(notPreferred)
        self.assertLess(preferredIndex, notPreferredIndex)


    def test_preferSHA(self):
        """Regular SHA (SHA-1) is preferred over SHA-256: it is faster, and
        equivalently secure in HMAC constructions.

        """
        shaSuites = [
            "ECDHE-RSA-AES128-SHA", "ECDHE-ECDSA-AES128-SHA",
            "DHE-RSA-AES128-SHA", "DHE-ECDSA-AES128-SHA",
        ]

        for suite in shaSuites:
            self.assertPreferred(suite, suite + "256")


    def test_dontPreferGCM(self):
        """Non-GCM suites are preferred over their GCM equivalent.

        """
        self.assertPreferred("ECDHE-RSA-AES128-SHA256",
                             "ECDHE-RSA-AES128-GCM-SHA256")
        self.assertPreferred("ECDHE-ECDSA-AES128-SHA256",
                             "ECDHE-ECDSA-AES128-GCM-SHA256")

        self.assertPreferred("DHE-ECDSA-AES128-SHA256",
                             "DHE-ECDSA-AES128-GCM-SHA256")
        self.assertPreferred("DHE-RSA-AES128-SHA256",
                             "DHE-RSA-AES128-GCM-SHA256")



    def test_mavericksSupport(self):
        """There is at least one ciphersuite that is supported by the OpenSSL
        0.9.8y that comes with OS X Mavericks.

        """
        inBoth = set(self.suites) & set(MAVERICKS_CIPHERS)
        self.assertTrue(inBoth)



# Ciphers supported by OpenSSL 0.9.8y, as shipped with OS X Mavericks
MAVERICKS_CIPHERS = [
    'DHE-RSA-AES256-SHA', 'DHE-DSS-AES256-SHA',
    'AES256-SHA',
    'EDH-RSA-DES-CBC3-SHA', 'EDH-DSS-DES-CBC3-SHA',
    'DES-CBC3-SHA', 'DES-CBC3-MD5',
    'DHE-RSA-AES128-SHA', 'DHE-DSS-AES128-SHA',
    'AES128-SHA',
    'DHE-RSA-SEED-SHA', 'DHE-DSS-SEED-SHA', 'SEED-SHA',

    # Now for the really bad ones:
    # RC2
    'RC2-CBC-MD5',
    # RC4
    'RC4-SHA', 'RC4-MD5', 'RC4-MD5',
    # DES
    'EDH-RSA-DES-CBC-SHA', 'EDH-DSS-DES-CBC-SHA',
    'DES-CBC-SHA', 'DES-CBC-MD5',
    # Export quality (not that DES, RC2, RC4 weren't bad already)
    'EXP-EDH-RSA-DES-CBC-SHA', 'EXP-EDH-DSS-DES-CBC-SHA', 'EXP-DES-CBC-SHA',
    'EXP-RC2-CBC-MD5', 'EXP-RC2-CBC-MD5',
    'EXP-RC4-MD5', 'EXP-RC4-MD5'
]

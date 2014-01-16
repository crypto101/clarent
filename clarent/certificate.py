"""
Tools for creating certificates.
"""
from datetime import datetime
from OpenSSL.crypto import PKey, X509, dump_privatekey, dump_certificate
from OpenSSL.crypto import TYPE_RSA, FILETYPE_PEM
from OpenSSL.SSL import SSLv23_METHOD, OP_NO_SSLv2, OP_NO_SSLv3
from twisted.internet.ssl import PrivateCertificate


def _makeCertificate(key, email, _utcnow=datetime.utcnow):
    """Make the certificate for the client using the given key and e-mail
    address.

    """
    # Create a certificate for this key.
    cert = X509()
    cert.set_pubkey(key)

    # Set the subject.
    subject = cert.get_subject()
    subject.CN = u"Crypto 101 Client"
    subject.emailAddress = email

    # Expiration dates. Mandatory.
    now = _utcnow()
    start = now.replace(hour=0, minute=0, second=0)
    cert.set_notBefore(start.strftime(_ASN1_GENERALIZEDTIME_FORMAT))
    end = start.replace(year=start.year + 5)
    cert.set_notAfter(end.strftime(_ASN1_GENERALIZEDTIME_FORMAT))

    # Self-sign.
    cert.set_issuer(cert.get_subject())
    cert.sign(key, "sha512")

    return cert


_ASN1_GENERALIZEDTIME_FORMAT = "%Y%m%d%H%M%SZ"


def _generateKey(_PKey=PKey):
    """Generate a 4096-bit RSA key.

    """
    key = _PKey()
    key.generate_key(TYPE_RSA, 4096)
    return key


def makeCredentials(path, email):
    """Make credentials for the client from given e-mail address and store
    them in the directory at path.

    """
    key = _generateKey()
    cert = _makeCertificate(key, email)

    certPath = path.child("client.pem")
    certPath.alwaysCreate = True

    with certPath.open("wb") as pemFile:
        pemFile.write(dump_privatekey(FILETYPE_PEM, key))
        pemFile.write(dump_certificate(FILETYPE_PEM, cert))



def getContextFactory(path):
    """Get a context factory for the client from keys already stored at
    path.

    Raises IOError if the credentials didn't exist.

    """
    with path.child("client.pem").open() as pemFile:
        cert = PrivateCertificate.loadPEM(pemFile.read())

    certOptions = cert.options() # TODO: verify server cert (see #1)
    certOptions.method = SSLv23_METHOD
    ctxFactory = SecureCiphersContextFactory(certOptions)
    return ctxFactory



class SecureCiphersContextFactory(object):
    """A context factory to limit SSL/TLS connections to secure
    ciphersuites.

    This wraps another context factory. When asked for a context, it
    asks the wrapped context factory for one, and then limits the
    context factory to only using secure ciphersuites. This also
    disables SSLv2 and SSLv3 ciphersuites, since they contain known
    issues.

    """
    def __init__(self, ctxFactory):
        self.ctxFactory = ctxFactory


    def getContext(self):
        ctx = self.ctxFactory.getContext()
        ctx.set_options(OP_NO_SSLv2|OP_NO_SSLv3)
        ctx.set_cipher_list(ciphersuites)
        return ctx



# Ciphersuites, based on Qualys' SSL/TLS Deployment Best Practices
# https://www.ssllabs.com/downloads/SSL_TLS_Deployment_Best_Practices_1.3.pdf
# Exceptions: Our RSA keys are bigger than recommended (4096 vs 2048).
# Since we can multiplex everything over a single connection, this
# doesn't really matter as much. Also, GCM is not as preferred,
# because GHASH is apparently very hard to implement without leaking
# timing information. It's still available, so that clients who know
# that theirs is good (i.e. they have a hardware implementation) can
# still get it.
ciphersuites = ":".join((
    # Fast, PFS, secure. Yay!
    "ECDHE-RSA-AES128-SHA", "ECDHE-ECDSA-AES128-SHA",
    # SHA-256 (equal to SHA-1, in HMAC construction)
    "ECDHE-RSA-AES128-SHA256", "ECDHE-ECDSA-AES128-SHA256",
    # GCM last (due to timing vulns in most GHASH implementations)
    "ECDHE-RSA-AES128-GCM-SHA256", "ECDHE-ECDSA-AES128-GCM-SHA256",

    # Same spiel, except with ECDHE -> DHE:
    "DHE-RSA-AES128-SHA", "DHE-ECDSA-AES128-SHA",
    "DHE-RSA-AES128-SHA256", "DHE-ECDSA-AES128-SHA256",
    "DHE-RSA-AES128-GCM-SHA256", "DHE-ECDSA-AES128-GCM-SHA256",
))

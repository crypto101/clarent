"""
Tools for creating certificates.
"""
from datetime import datetime
from OpenSSL.crypto import PKey, X509, dump_privatekey, dump_certificate
from OpenSSL.crypto import TYPE_RSA, FILETYPE_PEM
from twisted.internet.ssl import PrivateCertificate


def _makeCertificate(key, email, _utcnow=datetime.utcnow):
    """Make the certificate for the given key and e-mail address.

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
    """Make credentials from given e-mail address and store them in the
    directory at path.

    """
    key = _generateKey()
    cert = _makeCertificate(key, email)

    with path.child("client.pem").open("wb") as pemFile:
        pemFile.write(dump_privatekey(FILETYPE_PEM, key))
        pemFile.write(dump_certificate(FILETYPE_PEM, cert))



def getContextFactory(path):
    """Get a context factory from keys already stored at path.

    """
    with path.child("client.pem").open() as pemFile:
        cert = PrivateCertificate.loadPEM(pemFile.read())

    return cert.options() # TODO: verify server cert (see #1)

"""
Tools for creating certificates.
"""
from OpenSSL.crypto import PKey, TYPE_RSA, X509
from datetime import datetime


def makeCertificate(key, email, _utcnow=datetime.utcnow):
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


def generateKey(_PKey=PKey):
    """Generate a 4096-bit RSA key.

    """
    key = _PKey()
    key.generate_key(TYPE_RSA, 4096)
    return key

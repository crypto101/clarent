"""
Tools for creating certificates.
"""
from OpenSSL.crypto import PKey, TYPE_RSA, X509


def makeCertificate(key, email):
    """Make the certificate for the given key and e-mail address.

    """
    # Create a certificate for this key.
    cert = X509()
    cert.set_pubkey(key)

    # Set the subject.
    subject = cert.get_subject()
    subject.CN = u"Crypto 101 Client"
    subject.emailAddress = email

    # Self-sign.
    cert.set_issuer(cert.get_subject())
    cert.sign(key, "sha512")

    return cert


def generateKey(_PKey=PKey):
    """Generate a 4096-bit RSA key.

    """
    key = _PKey()
    key.generate_key(TYPE_RSA, 4096)
    return key

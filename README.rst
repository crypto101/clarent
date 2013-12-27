=========
 clarent
=========

.. image:: https://dl.dropbox.com/u/38476311/Logos/clarent.png

clarent is the home of the shared parts between merlyn_ and arthur_.
It is built as part of Crypto 101, the introductory book on
cryptography.

Changelog
=========

0.0.11
------

Improvements to certificate code:

- The context factory returned by ``getContextFactory`` now uses
  ``SSLv23_METHOD``. This also allows TLSv1.1 and TLSv1.2. Previously,
  it used Twisted's ``OpenSSLCertificateOptions``'s default, which is
  ``TLSv1_METHOD``, which means "TLSv1.0 only". This caused an
  incompatibility between clients using this code and ``merlyn``,
  which used ``SSLv23_METHOD``.
- ``SecureCiphersContextFactory`` now sets ``OP_NO_SSLv2`` as well as
  ``OP_NO_SSLv3``, since those contain known security issues.

Furthermore, extensive tests were added for:

- Verifying the behavior of ``SecureCiphersContextFactory``
- Verifying the preferred ciphersuite list

0.0.10
------

Moved dependencies into ``setup.py``. This should make ``clarent``
easier to install.

0.0.9
-----

Calling ``makeCredentials`` when the credentials already exists now
raises an exception; previously, the old credentials were silently
overwritten. This wasn't an issue due to the way callers used this
function previously, but can be an issue for future implementations.

0.0.8
-----

Added an SSL context factory that wraps other context factories, but
limits them to secure ciphers.

0.0.7
-----

- Added ``clarent.path``, gets data paths where you can dump some stuff.
- ``getContextFactory`` and ``makeCredentials`` are now citizens of
  ``clarent.certificate``.

0.0.6
-----

Bugfix: clarent no longer produces certificates without validity
periods (``notBefore`` and ``notAfter``). While silently dumping these
certs to disk appeared to succeed (yay, OpenSSL!), the produced file
would blow up any tool trying to read it, be it PyOpenSSL or the
``openssl x509`` command line tool.

This bug was fixed by adding ``notBefore`` and ``notAfter``. A unit
test was added that does nothing but dump and load the produced
certificate as well.

0.0.5
-----

- Removed the authentication API; all authentication is now done using
  TLS certificates.
- Added tools for making TLS keys and certificates.

0.0.4
-----

Fixes for the tests of the auth API.

0.0.3
-----

New TOFU-POP auth API.

0.0.2
-----

Drastically simplified exercise interface: no more multiple steps,
just rendering and asynchronous notification when they've been
completed. Completion happens out-of-band: users are asynchronously
notified when that happens.

0.0.1
-----

Initial version; includes the usual tox-based CI stuff.

Features:

- Exercise API AMP commands and exceptions, with tests, from merlin

Whence the name?
================

The server side to this is called merlyn_, because the step-by-step
oracle-like model reminded me of Merlin in the AM complexity class and
`Arthur-Merlin protocols`_. (It's not spelled the usual Merlin,
because that primo PyPI real estate was already taken up by some weird
setuptools fork.)

 Arthur was named afterwards, since it's the other side of the
Arthur-Merlin protocol. I decided to keep the trend; Clarent was King
Arthur's ceremonial sword.

.. _merlyn: https://github.com/crypto101/merlyn
.. _arthur: https://github.com/crypto101/arthur
.. _`Arthur-Merlin protocols`: https://en.wikipedia.org/wiki/Merlin-Arthur_protocol

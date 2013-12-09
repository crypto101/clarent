=========
 clarent
=========

.. image:: https://dl.dropbox.com/u/38476311/Logos/clarent.png

clarent is the home of the shared parts between merlyn_ and arthur_.
It is built as part of Crypto 101, the introductory book on
cryptography.

Changelog
=========

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

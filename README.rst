.. start-include

======
xpring
======

The Xpring SDK for Python.

.. image:: https://travis-ci.org/thejohnfreeman/xpring-py.svg?branch=master
   :target: https://travis-ci.org/thejohnfreeman/xpring-py
   :alt: Build status: Linux and OSX

.. image:: https://ci.appveyor.com/api/projects/status/github/thejohnfreeman/xpring-py?branch=master&svg=true
   :target: https://ci.appveyor.com/project/thejohnfreeman/xpring-py
   :alt: Build status: Windows

.. image:: https://readthedocs.org/projects/xpring-py/badge/?version=latest
   :target: https://xpring-py.readthedocs.io/
   :alt: Documentation status

.. image:: https://img.shields.io/pypi/v/xpring.svg
   :target: https://pypi.org/project/xpring/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/xpring.svg
   :target: https://pypi.org/project/xpring/
   :alt: Python versions supported


Install
=======

.. code-block:: shell

   pip install xpring


API
===

------
Wallet
------

Construct
---------

You can construct a :class:`Wallet` from its seed.
If you do not have your own wallet yet, you can `generate one with some free
XRP on the testnet`__.

.. __: https://xrpl.org/xrp-testnet-faucet.html

.. code-block:: python

   import xpring

   seed = 'sEdSKaCy2JT7JaM7v95H9SxkhP9wS2r'
   wallet = xpring.Wallet.from_seed(seed)
   print(wallet.public_key)
   # ED01FA53FA5A7E77798F882ECE20B1ABC00BB358A9E55A202D0D0676BD0CE37A63
   print(wallet.private_key)
   # EDB4C4E046826BD26190D09715FC31F4E6A728204EADD112905B08B14B7F15C4F3


Sign / Verify
-------------

A :class:`Wallet` can sign and verify arbitrary bytes, but you'll generally
want to leave these low-level responsibilities to the :class:`Client`.

.. code-block:: python

   message = bytes.fromhex('DEADBEEF')
   signature = wallet.sign(message)
   wallet.verify(message, signature)
   # True


------
Client
------

:class:`Client` is the gateway into the XRP Ledger.

Construct
---------

:class:`Client` is constructed with the URL of a Xpring server.
You may use the one operated by Ripple for the XRP testnet.

.. code-block:: python

   url = 'grpc.xpring.tech:80'
   client = xpring.Client.from_url(url)


Balance
-------

.. code-block:: python

   address = 'r3v29rxf54cave7ooQE6eE7G5VFXofKZT7'
   client.get_balance(address).balance
   # 1000


.. end-include


Develop
=======

------------
Dependencies
------------

The protocol buffers are in a submodule:

.. code-block:: shell

   git submodule init

Use Poetry_ to install dependencies and build the protocol buffers:

.. code-block:: shell

   poetry install
   poetry run invoke proto

.. _Poetry: https://python-poetry.org/docs/

-----
Tasks
-----

There are several Invoke_ tasks:

.. _Invoke: http://www.pyinvoke.org/

.. code-block:: shell

   poetry run invoke <task>

- ``test``: Pytest_ with coverage and doctests.
- ``lint``: Mypy_, Pylint_, and Pydocstyle_.
- ``serve``: Serve the docs locally and rebuild them on file changes.

.. _Pytest: https://docs.pytest.org/
.. _Mypy: https://mypy.readthedocs.io/
.. _Pylint: https://www.pylint.org/
.. _Pydocstyle: http://www.pydocstyle.org/

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

   pip install xpring[py]


API
===

------
Wallet
------

Construct
---------

You can construct a ``Wallet`` from its seed.
If you do not have your own wallet yet, you can `generate one with some free
XRP on the testnet`__.

.. __: https://xrpl.org/xrp-testnet-faucet.html

.. code-block:: python

   import xpring

   seed = 'sEdSKaCy2JT7JaM7v95H9SxkhP9wS2r'
   wallet = xpring.Wallet.from_seed(seed)
   print(wallet.private_key.hex())
   # b4c4e046826bd26190d09715fc31f4e6a728204eadd112905b08b14b7f15c4f3
   print(wallet.public_key.hex())
   # ed01fa53fa5a7e77798f882ece20b1abc00bb358a9e55a202d0d0676bd0ce37a63
   print(wallet.account_id.hex())
   # d28b177e48d9a8d057e70f7e464b498367281b98
   print(wallet.address)
   # rLUEXYuLiQptky37CqLcm9USQpPiz5rkpD


Sign / Verify
-------------

A ``Wallet`` can sign and verify arbitrary bytes, but you'll generally
want to leave these low-level responsibilities to the ``Client``.

.. code-block:: python

   message = bytes.fromhex('DEADBEEF')
   signature = wallet.sign(message)
   wallet.verify(message, signature)
   # True


------
Client
------

``Client`` is the gateway to the XRP Ledger.
It is constructed with the URL of the gRPC service of a rippled_ server.
If you are running the server yourself,
you need to configure the ``[port_grpc]`` stanza in your configuration file.
In the example_ configuration file, it is commented_ out.

.. _rippled: https://github.com/ripple/rippled
.. _example: https://github.com/ripple/rippled/blob/develop/cfg/rippled-example.cfg
.. _commented: https://github.com/ripple/rippled/blob/0c6d380780ae368a2236a2e8e3e42efa4a1d2b46/cfg/rippled-example.cfg#L1181-L1183

.. code-block:: python

   # url = 'main.xrp.xpring.io:50051' # Mainnet
   url = 'test.xrp.xpring.io:50051' # Testnet
   client = xpring.Client.from_url(url)


Account
-------

.. code-block:: python

   >>> client.get_account(wallet.address)
   account_data {
     account {
       value {
         address: "rDuKotkyx18D5WqWCA4mVhRWK2YLqDFKaY"
       }
     }
     balance {
       value {
         xrp_amount {
           drops: 999999820
         }
       }
     }
     sequence: {
       value: 10
     }
     flags {
     }
     owner_count {
     }
     previous_transaction_id {
       value: b"..."
     }
     previous_transaction_ledger_sequence {
       value: 4845872
     }
   }
   ledger_index: 4869818


Fee
---

.. code-block:: python

   >>> client.get_fee()
   current_ledger_size: 6
   fee {
     base_fee {
       drops: 10
     }
     median_fee {
       drops: 5000
     }
     minimum_fee {
       drops: 10
     }
     open_ledger_fee {
       drops: 10
     }
   }
   expected_ledger_size: 25
   ledger_current_index: 4869844
   levels {
     median_level: 128000
     minimum_level: 256
     open_ledger_level: 256
     reference_level: 256
   }
   max_queue_size: 2000


Submit
------

.. code-block:: python

   >>> unsigned_transaction = {
   ...     'Account': 'rDuKotkyx18D5WqWCA4mVhRWK2YLqDFKaY',
   ...     'Amount': '10',
   ...     'Destination': 'rNJDvXkaBRwJYdeEcx9pchE2SecMkH3FLz',
   ...     'Fee': '10',
   ...     'Flags': 0x80000000,
   ...     'Sequence': 9,
   ...     'TransactionType': 'Payment'
   ... }
   >>> signed_transaction = wallet.sign_transaction(unsigned_transaction)
   >>> client.submit(signed_transaction)
   engine_result {
     result_type: RESULT_TYPE_TES
     result: "tesSUCCESS"
   }
   engine_result_message: "The transaction was applied. Only final in a validated ledger."
   hash: b"..."
   >>> client.submit(signed_transaction)
   engine_result {
     result_type: RESULT_TYPE_TEF
     result: "tefPAST_SEQ"
   }
   engine_result_code: -190
   engine_result_message: "This sequence number has already passed."
   hash: b"..."


Transaction
-----------

.. code-block:: python

   >>> txid = bytes.fromhex(signed_transaction['hash'])
   >>> client.get_transaction(txid)
   transaction {
     account {
       value {
         address: "rDuKotkyx18D5WqWCA4mVhRWK2YLqDFKaY"
       }
     }
     fee {
       drops: 10
     }
     sequence {
       value: 10
     }
     payment {
       amount {
         value {
           xrp_amount {
             drops: 10
           }
         }
       }
       destination {
         value {
           address: "rNJDvXkaBRwJYdeEcx9pchE2SecMkH3FLz"
         }
       }
     }
     signing_public_key {
       value: b"..."
     }
     transaction_signature {
       value: b"..."
     }
     flags {
       value: 2147483648
     }
   }
   ledger_index: 5124377
   hash: b"..."
   validated: true
   meta {
     transaction_index: 1
     transaction_result {
       result_type: RESULT_TYPE_TES
       result: "tesSUCCESS"
     }
     affected_nodes {
       ledger_entry_type: LEDGER_ENTRY_TYPE_ACCOUNT_ROOT
       ledger_index: b"..."
       modified_node {
         final_fields {
           account_root {
             account {
               value {
                 address: "rNJDvXkaBRwJYdeEcx9pchE2SecMkH3FLz"
               }
             }
             balance {
               value {
                 xrp_amount {
                   drops: 1000000100
                 }
               }
             }
             sequence {
               value: 1
             }
             flags {
             }
             owner_count {
             }
           }
         }
         previous_fields {
           account_root {
             balance {
               value {
                 xrp_amount {
                   drops: 1000000090
                 }
               }
             }
           }
         }
         previous_transaction_id {
           value: b"..."
         }
         previous_transaction_ledger_sequence {
           value: 4845872
         }
       }
     }
     affected_nodes {
       ledger_entry_type: LEDGER_ENTRY_TYPE_ACCOUNT_ROOT
       ledger_index: b"..."
       modified_node {
         final_fields {
           account_root {
             account {
               value {
                 address: "rDuKotkyx18D5WqWCA4mVhRWK2YLqDFKaY"
               }
             }
             balance {
               value {
                 xrp_amount {
                   drops: 999999800
                 }
               }
             }
             sequence {
               value: 11
             }
             flags {
             }
             owner_count {
             }
           }
         }
         previous_fields {
           account_root {
             balance {
               value {
                 xrp_amount {
                   drops: 999999820
                 }
               }
             }
             sequence {
               value: 10
             }
           }
         }
         previous_transaction_id {
           value: b"..."
         }
         previous_transaction_ledger_sequence {
           value: 4845872
         }
       }
     }
     delivered_amount {
       value {
         xrp_amount {
           drops: 10
         }
       }
     }
   }
   date {
     value: 636581642
   }


.. end-include

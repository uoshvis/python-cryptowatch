==================
python-cryptowatch
==================

This is an unofficial Python wrapper for the `Cryptowatch public Data API <https://cryptowat.ch/docs/api>`_. Cryptowatch is a cryptocurrency charting and trading platform owned by `Kraken <https://www.kraken.com/>`_.


Source code
  https://github.com/uoshvis/python-cryptowatch

Documentation
  https://python-cryptowatch.readthedocs.io/en/latest/


Quick Start
-----------

.. code:: python

    from cryptowatch.api_client import Client
    client = Client()

    #get assets
    assets = get_assets()

    #get markets which have btc as base or quote
    assets_btc = get_assets('btc')


For more `check out the documentation <https://python-cryptowatch.readthedocs.io/en/latest/>`_.

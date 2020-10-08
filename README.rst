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

    # get assets
    assets = client.get_assets()

    # get markets which have btc as base or quote
    assets_btc = client.get_assets('btc')

    """
    Returns a market's OHLC candlestick data.
    This represents a 1-hour candle starting at 1594087200 and ending at 1602179348.
    """

    data = {
        'exchange': 'gdax',
        'pair': 'btcusd',
        'route': 'ohlc',
        'params': {
            'before': 1602179348,
            'after': 1594087200,
            'periods': '3600'}
    }

    market = client.get_markets(data=data)

For more `check out the documentation <https://python-cryptowatch.readthedocs.io/en/latest/>`_.

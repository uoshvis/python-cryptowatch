import requests
from urllib.parse import urlencode, quote_plus
from .exceptions import CryptowatchAPIException, CryptowatchRequestException


class Client(object):

    API_URL = 'https://api.cryptowat.ch'
    MARKET_ROUTES = ['price', 'summary', 'orderbook', 'trades', 'ohlc']
    PARAM_ROUTES = ['trades', 'ohlc']

    def __init__(self):
        self.uri = 'https://api.cryptowat.ch'
        self.session = self._init_session()

    def _init_session(self):
        session = requests.Session()
        session.headers.update({'Accept': 'application/json',
                                'User-Agent': 'cryptowatch/python'})
        return session

    def _encode_params(self, **kwargs):
        data = kwargs.get('data', None)
        payload = {}
        if data['route'] == 'trades':
            params = data['params']
            if 'limit' in params:
                payload['limit'] = params['limit']
            if 'since' in params:
                payload['since'] = params['since']
        elif data['route'] == 'ohlc':
            params = data['params']
            if 'before' in params:
                payload['before'] = params['before']
            if 'after' in params:
                payload['after'] = params['after']
            if 'periods' in params:
                payload['periods'] = params['periods']

        return urlencode(payload, quote_via=quote_plus)

    def _request(self, method, uri):
        response = getattr(self.session, method)(uri)
        return self._handle_response(response)

    def _create_uri(self, path, symbol):
        uri = self.API_URL + '/' + path
        if symbol:
            uri += '/' + symbol
        return uri

    def _request_api(self, method, path, symbol):
        uri = self._create_uri(path, symbol)
        print(uri)
        return self._request(method, uri)

    def _get(self, path, symbol=None):
        return self._request_api('get', path, symbol)

    def _handle_response(self, response):
        if not str(response.status_code).startswith('2'):
            raise CryptowatchAPIException(response)
        try:
            return response.json()
        except ValueError:
            raise CryptowatchRequestException('Invalid Response: %s' % response.text)

    def get_assets(self, asset=None):
        """Returns all assets (crypto and fiat).

        :returns: list - List of asset dictionaries

        .. code-block:: python

            {
              "result": [
                {
                  "symbol": "aud",
                  "name": "Australian Dollar",
                  "fiat": true,
                  "route": "https://api.cryptowat.ch/assets/aud"
                },
                {
                  "symbol": "etc",
                  "name": "Ethereum Classic",
                  "fiat": false,
                  "route": "https://api.cryptowat.ch/assets/etc"
                },
                ...
              ]
            }

        If asset symbol is given:

        .. code-block:: python

            get_assets('btc')

        Lists all markets which have this asset as a base or quote:

        .. code-block:: python

            {
              "result": {
                "symbol": "btc",
                "name": "Bitcoin",
                "fiat": false,
                "markets": {
                  "base": [
                    {
                      "exchange": "bitfinex",
                      "pair": "btcusd",
                      "active": true,
                      "route": "https://api.cryptowat.ch/markets/bitfinex/btcusd"
                    },
                    {
                      "exchange": "gdax",
                      "pair": "btcusd",
                      "route": "https://api.cryptowat.ch/markets/gdax/btcusd"
                    },
                    ...
                  ],
                  "quote": [
                    {
                      "exchange": "bitfinex",
                      "pair": "ltcbtc",
                      "active": true,
                      "route": "https://api.cryptowat.ch/markets/bitfinex/ltcbtc"
                    },
                    {
                      "exchange": "bitfinex",
                      "pair": "ethbtc",
                      "active": true,
                      "route": "https://api.cryptowat.ch/markets/bitfinex/ethbtc"
                    },
                    ...
                  ]
                }
              }
            }

        """

        if asset:
            return self._get('assets', asset)

        return self._get('assets')

    def get_pairs(self, pair=None):
        """Returns all pairs (in no particular order).

        :returns: list - List of pairs dictionaries

        .. code-block:: python

            {
              "result": [
                {
                  "symbol": "xmrusd",
                  "id": 82,
                  "base": {
                    "symbol": "xmr",
                    "name": "Monero",
                    "fiat": false,
                    "route": "https://api.cryptowat.ch/assets/xmr"
                  },
                  "quote": {
                    "symbol": "usd",
                    "name": "United States dollar",
                    "fiat": true,
                    "route": "https://api.cryptowat.ch/assets/usd"
                  },
                  "route": "https://api.cryptowat.ch/pairs/xmrusd"
                },
                {
                  "symbol": "ltcusd",
                  "id": 189,
                  "base": {
                    "symbol": "ltc",
                    "name": "Litecoin",
                    "fiat": false,
                    "route": "https://api.cryptowat.ch/assets/ltc"
                  },
                  "quote": {
                    "symbol": "usd",
                    "name": "United States dollar",
                    "fiat": true,
                    "route": "https://api.cryptowat.ch/assets/usd"
                  },
                  "route": "https://api.cryptowat.ch/pairs/ltcusd"
                },
                ...
              ]
            }

        If pair is given:

        .. code-block:: python

            get_pairs('ethbtc')

        Lists all markets for this pair:

        .. code-block:: python

            {
              "result": {
                "symbol": "ethbtc",
                "id": 23,
                "base": {
                  "symbol": "eth",
                  "name": "Ethereum",
                  "isFiat": false,
                  "route": "https://api.cryptowat.ch/assets/eth"
                },
                "quote": {
                  "symbol": "btc",
                  "name": "Bitcoin",
                  "isFiat": false,
                  "route": "https://api.cryptowat.ch/assets/btc"
                },
                "route": "https://api.cryptowat.ch/pairs/ethbtc",
                "markets": [
                  {
                    "exchange": "bitfinex",
                    "pair": "ethbtc",
                    "active": true,
                    "route": "https://api.cryptowat.ch/markets/bitfinex/ethbtc"
                  },
                  {
                    "exchange": "gdax",
                    "pair": "ethbtc",
                    "active": true,
                    "route": "https://api.cryptowat.ch/markets/gdax/ethbtc"
                  },
                  ...
                ]
              }
            }

        """

        if pair:
            return self._get('pairs', pair)

        return self._get('pairs')

    def get_exchanges(self, exchange=None):
        """Returns a list of all supported exchanges.


        :returns: list - List of exchanges dictionaries

        .. code-block:: python

            {
              "result": [
                {
                  "symbol": "bitfinex",
                  "name": "Bitfinex",
                  "active": true,
                  "route": "https://api.cryptowat.ch/exchanges/bitfinex"
                },
                {
                  "symbol": "gdax",
                  "name": "GDAX",
                  "active": true,
                  "route": "https://api.cryptowat.ch/exchanges/gdax"
                },
                ...
              ]
            }

        If exchange name is given:

        .. code-block:: python

            get_exchanges('kraken')

        Lists a single exchange, with associated routes:

        .. code-block:: python

            {
              "result": {
                "id": "kraken",
                "name": "Kraken",
                "active": true,
                "routes": {
                  "markets": "https://api.cryptowat.ch/markets/kraken"
                }
              }
            }

        """
        if exchange:
            return self._get('exchanges', exchange)

        return self._get('exchanges')

    def get_markets(self, path=None, **kwargs):
        """Returns a list of all supported markets.

        :returns: list - List of markets dictionaries

        .. code-block:: python

            {
              "result": [
                {
                  "exchange": "bitfinex",
                  "pair": "btcusd",
                  "active": true,
                  "route": "https://api.cryptowat.ch/markets/bitfinex/btcusd"
                },
                {
                  "exchange": "bitfinex",
                  "pair": "ltcusd"
                  "active": true,
                  "route": "https://api.cryptowat.ch/markets/bitfinex/ltcusd"
                },
                {
                  "exchange": "bitfinex",
                  "pair": "ltcbtc"
                  "active": true,
                  "route": "https://api.cryptowat.ch/markets/bitfinex/ltcbtc"
                },
                ...
              ]
            }

        To get the supported markets for only a specific exchange:

        .. code-block:: python

            get_markets('kraken')

        To get a single market, with associated routes
        pass a data dictionary with specific values:

        .. code-block:: python

            data = {
                'exchange': 'gdax',
                'pair': 'btcusd'
            }

            get_markets(data=data)

        This returns a single market, with associated routes:

        .. code-block:: python

            {
              "result": {
                "exchange": "gdax",
                "pair": "btcusd",
                "active": true,
                "routes": {
                  "price": "https://api.cryptowat.ch/markets/gdax/btcusd/price",
                  "summary": "https://api.cryptowat.ch/markets/gdax/btcusd/summary",
                  "orderbook": "https://api.cryptowat.ch/markets/gdax/btcusd/orderbook",
                  "trades": "https://api.cryptowat.ch/markets/gdax/btcusd/trades",
                  "ohlc": "https://api.cryptowat.ch/markets/gdax/btcusd/ohlc"
                }
              }
            }

        **Price**

        To get a market’s last price
        pass a data dictionary with specific values:

        .. code-block:: python

            data = {
                'exchange': 'gdax',
                'pair': 'btcusd',
                'route': 'price'
            }

            get_markets(data=data)

        This returns a last price:

        .. code-block:: python

            {
              "result": {
                "price": 780.63
              }
            }

        **Summary**

        To get a market’s last price as well as
        other stats based on a 24-hour sliding window
        pass a data dictionary with specific values:

        .. code-block:: python

            data = {
                'exchange': 'gdax',
                'pair': 'btcusd',
                'route': 'summary'
            }

            get_markets(data=data)

        This returns:

        .. code-block:: python

            {
              "result": {
                "price":{
                  "last": 780.31,
                  "high": 790.34,
                  "low": 772.76,
                  "change": {
                    "percentage": 0.0014373838,
                    "absolute": 1.12
                  }
                },
                "volume": 5345.0415
              }
            }

        **Trades**

        To get most recent trades (incrementing chronologically).
        'route': 'trades' accepts 'limit' and 'since' parameters.

          .. code-block:: python

            data = {
                'exchange': 'gdax',
                'pair': 'btcusd',
                'route': 'trades'
                'params': {'limit': 10, 'since': 1481663244 }
            }

            get_markets(data=data)

        This returns:

          .. code-block:: python

              {
                "result": [
                  [
                    0,
                    1481676478,
                    734.39,
                    0.1249
                  ],
                  [
                    0,
                    1481676537,
                    734.394,
                    0.0744
                  ],
                  [
                    0,
                    1481676581,
                    734.396,
                    0.1
                  ],
                  [
                    0,
                    1481676602,
                    733.45,
                    0.061
                  ],
                  ...
                ]
              }

        Trades are lists of numbers in this order:

        .. code-block:: python

          [ ID, Timestamp, Price, Amount ]

        **Ordebook**

        To get market's order book use 'orderbook' route:

        .. code-block:: python

          data = {
                'exchange': 'gdax',
                'pair': 'btcusd',
                'route': 'orderbook'
            }

        Example return:

        .. code-block:: python

          {
            "result": {
              "asks": [
                [
                  733.73,
                  2.251
                ],
                [
                  733.731,
                  7.829
                ],
                [
                  733.899,
                  1.417
                ],
                ...
              ],
              "bids": [
                [
                  733.62,
                  0.273
                ],
                ...
              ]
            ]
          }

      Orders are lists of numbers in this order:

        .. code-block:: python

          [ Price, Amount ]

      **OHLC**

      To get a market's OHLC candlestick data.
      Params supported:
      'before': UNIX timestamp,
      'after': UNIX timestamp,
      'periods': Comma-separated integers  60,180,108000

      .. code-block:: python

        data = {
            'exchange': 'gdax',
            'pair': 'btcusd',
            'route': 'ohlc'
            'params': {
              'before': 1481663244,
              'after': 1481663244,
              'periods': '60,120'
              }
        }

        get_markets(data=data)

      Return values are in list:

        .. code-block:: python

          [ CloseTime, OpenPrice, HighPrice, LowPrice, ClosePrice, Volume ]


        """

        data = kwargs.get('data', None)
        if data and isinstance(data, dict):
            if 'exchange' in data:
                path = data['exchange']
                if 'pair' in data:
                    path += '/' + data['pair']
                    if 'route' in data and data['route'] in self.MARKET_ROUTES:
                        path += '/' + data['route']
                        if data['route'] in self.PARAM_ROUTES and 'params' in data:
                            path += '?' + self._encode_params(path=path, data=data)
        if path:
            return self._get('markets', path)

        return self._get('markets')

    def get_aggregates(self, *args):
        if not args:
            raise ValueError('Use either "prices", or "summaries"')
        return self._get('markets', args[0])

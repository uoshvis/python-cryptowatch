"""Module related to the client interface to cryptowat.ch API."""

from urllib.parse import quote_plus, urlencode
import requests
from cryptowatch.exceptions import (
    CryptowatchAPIException,
    CryptowatchResponseException
)


class Client(object):
    """The public client to the cryptowat.ch api."""

    API_URL = 'https://api.cryptowat.ch'
    ROUTES_MARKET = ['price', 'summary', 'orderbook', 'trades', 'ohlc']
    ROUTES_PARAMS = ['trades', 'ohlc']
    ROUTES_AGGREGATE = ['prices', 'summaries']

    def __init__(self):
        self.uri = 'https://api.cryptowat.ch'
        self.session = self._init_session()

    @staticmethod
    def _init_session():
        session = requests.Session()
        session.headers.update({'Accept': 'application/json',
                                'User-Agent': 'cryptowatch/python'})
        return session

    @staticmethod
    def _encode_params(**kwargs):
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
        return self._request(method, uri)

    def _get(self, path, symbol=None):
        return self._request_api('get', path, symbol)

    @staticmethod
    def _handle_response(response):
        if not str(response.status_code).startswith('2'):
            raise CryptowatchAPIException(response)
        try:
            return response.json()
        except ValueError:
            raise CryptowatchResponseException('Invalid Response: %s' % response.text)

    def get_assets(self, asset=None):
        """An asset can be a crypto or fiat currency.

        **Index**

        .. code-block:: python

            get_assets()

        :returns: API response

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

        **Asset**

        Returns a single asset.
        Lists all markets which have this asset as a base or quote.

        .. code-block:: python

            get_assets('btc')

        :returns: API response

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
        """A pair of assets. Each pair has a base and a quote.
        For example, btceur has base btc and quote eur.

        **Index**

        All pairs (in no particular order).

        .. code-block:: python

          get_pairs()

        :returns: API response

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

        **Pair**

        Returns a single pair. Lists all markets for this pair.

        .. code-block:: python

            get_pairs('ethbtc')

        :returns: API response

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
        """Exchanges are where all the action happens!

      **Index**

      Returns a list of all supported exchanges.

      .. code-block:: python

        get_exchanges()

      :returns: API response

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

      **Exchange**

      Returns a single exchange, with associated routes.

      .. code-block:: python

        get_exchanges('kraken')

      :returns: API response

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

        """
      A market is a pair listed on an exchange.
      For example, pair btceur on exchange kraken is a market.

      **Index**

      Returns a list of all supported markets.

      .. code-block:: python

        get_markets()

      :returns: API response

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

      **Market**

      Returns a single market, with associated routes.

      :param exchange: required
      :type exchange: str
      :param pair: required
      :type pair: str

      .. code-block:: python

        data = {
            'exchange': 'gdax',
            'pair': 'btcusd'
        }

      .. code-block:: python

        get_markets(data=data)

      :returns: API response

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

      Returns a market’s last price.

      :param exchange: required
      :type exchange: str
      :param pair: required
      :type pair: str
      :param route: 'price'
      :type route: str

      .. code-block:: python

        data = {
            'exchange': 'gdax',
            'pair': 'btcusd',
            'route': 'price'
        }

      .. code-block:: python

        get_markets(data=data)

      :returns: API response

      .. code-block:: python

        {
          "result": {
            "price": 780.63
          }
        }

      **Summary**

      Returns a market’s last price as well as other stats
      based on a 24-hour sliding window.

      :param exchange: required
      :type exchange: str
      :param pair: required
      :type pair: str
      :param route: 'summary'
      :type route: str

      .. code-block:: python

        data = {
            'exchange': 'gdax',
            'pair': 'btcusd',
            'route': 'summary'
        }

      .. code-block:: python

        get_markets(data=data)

      :returns: API response

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

      Returns a market’s most recent trades, incrementing chronologically.

      :param exchange: required
      :type exchange: str
      :param pair: required
      :type pair: str
      :param route: 'trades'
      :type route: str
      :param params: supported params
      :type params: dict
      :param params.limit: limit amount of trades returned
      :type params.limit: int (defaults to 50)
      :param params.since: only return trades at or after this time.
      :type params.since: UNIX timestamp

      .. code-block:: python

        data = {
            'exchange': 'gdax',
            'pair': 'btcusd',
            'route': 'trades',
            'params': {'limit': 10, 'since': 1481663244 }
        }
      .. code-block:: python

        get_markets(data=data)

      :returns: API response

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

      **Order Book**

      To get market's order book use 'orderbook' route.

      :param exchange: required
      :type exchange: str
      :param pair: required
      :type pair: str
      :param route: 'orderbook'
      :type route: str

      .. code-block:: python

        data = {
              'exchange': 'gdax',
              'pair': 'btcusd',
              'route': 'orderbook'
          }

      :returns: API response

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

      Returns a market’s OHLC candlestick data.
      Returns data as lists of lists of numbers for each time period integer.

      :param exchange: required
      :type exchange: str
      :param pair: required
      :type pair: str
      :param route: 'ohlc'
      :type route: str
      :param params: supported params
      :type params: dict
      :param params.before: Only return candles opening before this time
      :type params.before: int (defaults to 50)
      :param params.after:  Only return candles opening after this time
      :type params.after: UNIX timestamp
      :param params.periods: return these time periods
      :type params.periods: Comma-separated integers  60,180,108000

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

      .. code-block:: python

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
                    if 'route' in data and data['route'] in self.ROUTES_MARKET:
                        path += '/' + data['route']
                        if data['route'] in self.ROUTES_PARAMS and 'params' in data:
                            path += '?' + self._encode_params(path=path, data=data)
        if path:
            return self._get('markets', path)

        return self._get('markets')

    def get_aggregates(self, *args):
        """Retrieves the prices and summaries of all markets
        on the site in a single request.

        **Prices**

        To get the current price for all supported markets use:

        .. code-block:: python

          get_aggregates('prices')

        :returns: API response

        .. code-block:: python

          {
            "result": {
              {
                "bitfinex:bfxbtc": 0.00067133,
                "bitfinex:bfxusd": 0.52929,
                "bitfinex:btcusd": 776.73,
                ...
              }
            }
          }

        **Summaries**

        To get the market summary for all supported markets use:

        .. code-block:: python

          get_aggregates('summaries')

        :returns: API response

        .. code-block:: python

          {
            "result": {
              {
                "bitfinex:bfxbtc": {
                  "price": {
                    "last": 0.00067133,
                    "high": 0.0006886,
                    "low": 0.00066753,
                    "change": {
                      "percentage": -0.02351996,
                      "absolute": -1.6169972e-05
                    }
                  },
                  "volume":84041.625
                },
                "bitfinex:bfxusd": {
                  ...
                },
                "bitfinex:btcusd": {
                  ...
                },
                ...
              }
            }
          }

        """
        if not args or args[0] not in self.ROUTES_AGGREGATE:
            raise ValueError('Use either "prices", or "summaries"')
        return self._get('markets', args[0])

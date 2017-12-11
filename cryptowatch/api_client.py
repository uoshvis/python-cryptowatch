import requests
from urllib.parse import urlencode, quote_plus


class Client(object):
    API_URL = 'https://api.cryptowat.ch'
    MARKET_ROUTES = ['price', 'summary', 'orderbook', 'trades', 'ohlc']
    PARAM_ROUTES = ['trades', 'ohlc']

    def __init__(self):
        self.uri = 'https://api.cryptowat.ch'
        self.session = self._init_session()
        # self.response = None

    def _init_session(self):
        session = requests.Session()
        session.headers.update({'Accept': 'application/json',
                                'User-Agent': 'cryptowatch/python'})
        return session

    def _request(self, method, uri):
        self.response = getattr(self.session, method)(uri)
        return self._handle_response(self.response)

    def _create_uri(self, path, symbol):
        uri = self.API_URL + '/' + path
        if symbol:
            uri = uri + '/' + symbol
        print(uri)
        return uri

    def _request_api(self, method, path, symbol):
        uri = self._create_uri(path, symbol)

        return self._request(method, uri)

    def _get(self, path, symbol=None):
        return self._request_api('get', path, symbol)

    def _handle_response(self, response):
        """Internal helper for handling API responses.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not str(response.status_code).startswith('2'):
            response.raise_for_status()
            # TODO raise exception   # try: return
        return response.json()

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

    def query(self, method, data=None):

        if data is None:
            data = {}

        urlpath = '/' + method

        return self._query(urlpath, data)

    def get_assets(self, asset=None):
        """Returns all assets (if no symbol provided).
        If symbol is given returns a single asset.
        Lists all markets which have this asset as a base or quote.

        :returns: list - List of product dictionaries
        """
        if asset:
            return self._get('assets', asset)

        return self._get('assets')

    def get_pairs(self, pair=None):
        """A pair of assets. Each pair has a base and a quote.
        For example, btceur has base btc and quote eur.


        :returns: list - List of product dictionaries
        """
        if pair:
            return self._get('pairs', pair)

        return self._get('pairs')

    def get_exchanges(self, exchange=None):
        """Returns a list of all supported exchanges.


        :returns: list - List of product dictionaries
        """
        if exchange:
            return self._get('exchanges', exchange)

        return self._get('exchanges')

    def get_markets(self, path, **kwargs):
        """Returns a list of all supported exchanges.

        :returns: list - List of product dictionaries
        """
        path = None
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

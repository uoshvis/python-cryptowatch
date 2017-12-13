from cryptowatch.api_client import Client
from cryptowatch.exceptions import CryptowatchAPIException, CryptowatchRequestException

import pytest
import requests_mock


client = Client()


@pytest.fixture
def assets_keys(scope='module'):
    return ['result', 'allowance']


def test_get_assets(assets_keys, symbol=None):
    """Test an API call to get assets' info """
    response = client.get_assets(symbol)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_get_assets_symbol(assets_keys, symbol='btc'):
    """Test an API call to get assets' info """
    response = client.get_assets(symbol)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_api_exception(assets_keys, symbol='invalid'):
    """Test API response Exception"""
    with pytest.raises(CryptowatchAPIException):
        client.get_assets(symbol)


def test_invalid_json(assets_keys, symbol='btc'):
    """Test Invalid response Exception"""

    with pytest.raises(CryptowatchRequestException):
        with requests_mock.mock() as m:
            m.get('https://api.cryptowat.ch/assets/btc', text='<head></html>')
            client.get_assets(symbol)


def test_get_single_exchange_market(assets_keys, symbol='kraken'):
    """Test an API call to get assets' info """
    response = client.get_markets(symbol)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_get_single_market(assets_keys):
    """Test an API call to get assets' info """
    data = {
        'exchange': 'gdax',
        'pair': 'btcusd'
    }
    response = client.get_markets(data=data)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_get_price(assets_keys):
    """Test an API call to get assets' info """
    data = {
        'exchange': 'gdax',
        'pair': 'btcusd',
        'route': 'price'
    }
    response = client.get_markets(data=data)
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_get_agg_prices(assets_keys):
    response = client.get_aggregates('prices')
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_get_agg_summaries(assets_keys):
    response = client.get_aggregates('summaries')
    assert isinstance(response, dict)
    assert set(assets_keys).issubset(response.keys())


def test_get_agg_summaries_exception():
    with pytest.raises(ValueError):
        client.get_aggregates('test')


def test_get_agg_summaries_exception_no_arg():
    with pytest.raises(ValueError):
        client.get_aggregates()

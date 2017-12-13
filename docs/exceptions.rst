Exceptions
==========

CryptowatchAPIException
-----------------------

On an API call error a binance.exceptions.BinanceAPIException will be raised.

The exception provides access to the

- `status_code` - response status code
- `reason` - response reason
- `response` - response object


CryptowatchResponseException
----------------------------

Raised if a non JSON response is returned

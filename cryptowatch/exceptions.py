"""Custom exceptions module."""


class CryptowatchAPIException(Exception):
    """Raised when the API response is not 2xx."""

    def __init__(self, response):
        super(CryptowatchAPIException, self).__init__()
        self.status_code = response.status_code
        self.reason = response.reason
        self.response = response

    def __str__(self):
        return 'APIError(code=%s): %s' % (self.status_code, self.reason)


class CryptowatchResponseException(Exception):
    """Raised for an invalid json response from the API"""

    def __init__(self, message):
        super(CryptowatchResponseException, self).__init__()
        self.message = message

    def __str__(self):
        return 'CryptowatchResponseException: %s' % self.message

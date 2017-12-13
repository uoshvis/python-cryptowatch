class CryptowatchAPIException(Exception):
    def __init__(self, response):
        self.status_code = response.status_code
        self.reason = response.reason
        self.response = response

    def __str__(self):
        return 'APIError(code=%s): %s' % (self.status_code, self.reason)


class CryptowatchResponseException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'CryptowatchResponseException: %s' % self.message

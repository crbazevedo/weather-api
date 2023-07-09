import httpx
import urllib
import logging

logger = logging.getLogger(__name__)

class HideSensitiveTransport(httpx.AsyncHTTPTransport):
    def __init__(self, sensitive_params=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sensitive_params = sensitive_params or []

    async def request(self, method, url, **kwargs):
        # Check if 'params' argument exists in kwargs
        if 'params' in kwargs:
            params = kwargs['params']
            filtered_params = params.copy()
            for param in self.sensitive_params:
                if param in filtered_params:
                    filtered_params[param] = "[FILTERED]"
            filtered_url = url
        else:
            # Remove sensitive parameters from the URL before it's logged
            parsed_url = list(urllib.parse.urlparse(url))
            query_params = dict(urllib.parse.parse_qsl(parsed_url[4]))
            for param in self.sensitive_params:
                if param in query_params:
                    query_params[param] = "[FILTERED]"
            parsed_url[4] = urllib.parse.urlencode(query_params)
            filtered_url = urllib.parse.urlunparse(parsed_url)

        # Use the filtered URL in the log message
        log_message = f"Sending request: {method} {filtered_url}"
        logger.info(log_message)

        # Send the actual request with the original URL and parameters
        return await super().request(method, url, **kwargs)
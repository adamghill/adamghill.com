from os import getenv


class HTTPSOnlyMiddleware:
    """
    Override request.is_secure() to return `True` based on a setting.

    Only use if you're **always** serving with HTTPS
    **and** SECURE_PROXY_SSL_HEADER is not suitable for your setup.

    Based on https://noumenal.es/notes/til/django/csrf-trusted-origins/ and
    https://gist.github.com/carltongibson/648099cd34b2c0a18e948c917a5c48fd.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # TODO: Add this to Coltrane bool settings
        if not request.is_secure() and getenv("COLTRANE_IS_SECURE") == "True":
            # Override `is_secure`
            print("set as secure")
            request.is_secure = lambda: True

        print("secure", request.is_secure())

        response = self.get_response(request)
        return response

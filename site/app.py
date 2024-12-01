#!/usr/bin/env python

from os import getenv

from coltrane import initialize, run

COMPRESS_FILTERS = {
    "css": [
        "refreshcss.filters.RefreshCSSFilter",
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.rJSMinFilter"],
}

SITES = {
    "adamghill": [
        "0.0.0.0:80",  # default for healthcheck
        "0.0.0.0:8020",
        "localhost:8020",
        "adamghill.localhost",
        "adamghill.com",
    ],
    "alldjango": [
        "0.0.0.0:8021",
        "localhost:8021",
        "alldjango.localhost",
        "alldjango.com",
    ],
}

wsgi = initialize(
    GITHUB_PERSONAL_ACCESS_TOKEN=getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
    COMPRESS_FILTERS=COMPRESS_FILTERS,
    COMPRESS_ENABLED=True,
    COLTRANE_SITES=SITES,
)


if __name__ == "__main__":
    run()

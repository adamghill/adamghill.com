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

wsgi = initialize(
    GITHUB_PERSONAL_ACCESS_TOKEN=getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
    COMPRESS_FILTERS=COMPRESS_FILTERS,
    COMPRESS_ENABLED=True,
)
print("wsgi", wsgi)

if __name__ == "__main__":
    print("called main")
    run()

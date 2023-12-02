#!/usr/bin/env python

from os import getenv

from coltrane import initialize
from django.core.management import execute_from_command_line

wsgi = initialize(
    GITHUB_PERSONAL_ACCESS_TOKEN=getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
    # INSTALLED_APPS=[
    #     "compressor",  # this can get removed once django-compressor is supported automatically
    # ],
    # SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https"),
    MIDDLEWARE=[
        "middleware.HTTPSOnlyMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.middleware.security.SecurityMiddleware",
        # "django.middleware.GZipMiddleware",
        # "django.middleware.ConditionalGetMiddleware",
        "django.middleware.common.CommonMiddleware",
        # "django.middleware.csrf.CsrfViewMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ],
)

if __name__ == "__main__":
    execute_from_command_line()

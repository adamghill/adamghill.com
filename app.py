#!/usr/bin/env python

from os import getenv

from coltrane import initialize
from django.core.management import execute_from_command_line

wsgi = initialize(
    GITHUB_PERSONAL_ACCESS_TOKEN=getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
)

if __name__ == "__main__":
    execute_from_command_line()

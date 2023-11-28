# adamghill.com

The website for adamghill.com. Built with `Coltrane` and ☕️.

# Run locally

- Install `Poetry`
- `cp .env.example .env` and update `.env` with a secret key
- `poe r` or `poetry run coltrane play`

# To build static site

`poetry run coltrane build`

# To develop with local `Coltrane`

1. `poetry remove coltrane`
1. Add `coltrane = { path="../coltrane", develop=true }` to `pyproject.toml`
1. `poetry lock && poetry install`

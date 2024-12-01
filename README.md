# adamghill.com

The website for adamghill.com. Built with `Coltrane` and ☕️.

# Run locally

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
1. `git clone` this repo
1. `cd` into the newly created directory
1. `cp .env.example .env`
1. Update `.env`
1. `uv run coltrane play`

# Add new site

1. `vim $(brew --prefix)/etc/Caddyfile`
1. Add something like ```
new-site.locahost {
    reverse_proxy localhost:8020
}```
1. `caddy validate --config $(brew --prefix)/etc/Caddyfile && brew services restart caddy`

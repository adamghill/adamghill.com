The websites for adamghill.com and alldjango.com. Built with `Coltrane` and ☕️.

# Run locally

1. Install `caddy` to allow nicer local domains for each site: `brew install caddy`
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
1. Install [just](https://docs.astral.sh/uv/getting-started/installation/)
1. `git clone` this repo
1. `cd` into the newly created directory
1. `cp .env.example .env`
1. Update `.env`
1. `just serve-adamghill` or `just serve-alldjango`

# Add new site

1. `vim $(brew --prefix)/etc/Caddyfile`
1. Add something like
```
new-site.locahost {
    reverse_proxy localhost:8029
}```
1. `caddy validate --config $(brew --prefix)/etc/Caddyfile && brew services restart caddy`

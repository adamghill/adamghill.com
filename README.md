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

# Run Docker site

1. `docker build -t adamghill . && docker run -e SECRET_KEY="secret" -e DEBUG=False -e COLTRANE_IS_SECURE=True -e ALLOWED_HOSTS="localhost,0.0.0.0" -p 8080:80 adamghill`

# Run Docker site with local coltrane

1. `cp -rf ../coltrane/* ./coltrane && docker build -t adamghill . && docker run -e SECRET_KEY="secret" -e DEBUG=False -e COLTRANE_IS_SECURE=True -e ALLOWED_HOSTS="localhost,0.0.0.0" -e CSRF_TRUSTED_ORIGINS="http://localhost:8080" -e COLTRANE_EXTRA_FILE_NAMES="robots.txt,isitwebscale.json" -p 8080:80 adamghill`



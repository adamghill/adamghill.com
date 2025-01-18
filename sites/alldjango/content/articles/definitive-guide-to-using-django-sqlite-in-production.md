---
template: base.html
title: The definitive guide to using Django with SQLite in production
date: 2025-01-18 10:33:16 -0400
categories: django python sqlite sqlite3 litestack
description: Run production Django sites with SQLite to reduce server costs and network latency.
---

I have been running Django sites in production under heavy load for over 10 years at my day job. We started with a MySQL database backend but, after running into a few issues, switched to PostgreSQL which has been rock-solid. I tend to use the same stack for side projects. Especially because, initially, most of my projects were hosted on Heroku and they had stellar support for PostgreSQL. Now, having bounced from Heroku to Render to Fly.io to [Digital Ocean](https://m.do.co/c/617d629f56c0) (with [CapRover](https://caprover.com/)) to [Hetzner](https://hetzner.cloud/?ref=2SkHDuMdo4Vt) (with [Coolify](https://coolify.io)), I am re-evaluating my default choice of database.

I currently have a managed PostgreSQL database at [Digital Ocean](https://m.do.co/c/617d629f56c0) which has worked well, but I have been looking into using [SQLite](https://www.sqlite.org/) in production to reduce server costs and network latency. And, since I'm not particularly DevOps-y, I do not want to be on the hook for maintaining my own PostgreSQL database. So, I have been investigating other solutions for my newest side project, [filmcliq.com](https://filmcliq.com).

## The Promise

There has been a lot of conversation about using SQLite as a production database for websites for the past few years, espeically in the Rails community with [Litestack](https://github.com/oldmoe/litestack). And now, in the latest version of Rails, SQLite has become the defacto backend for many parts of the stack.

The [Rails 8 release notes](https://rubyonrails.org/2024/11/7/rails-8-no-paas-required) details a lot of the "why" for using SQLite in production. But, mostly it comes down to: reduce the complexity of building and maintaining a website.

- No separate database server, e.g. PostgreSQL
- No separate cache server, e.g. redis
- No separate queue broker server, e.g. RabbitMQ

_Especially_ for side projects with limited traffic requirements and scaling concerns, the promise of SQLite is that it can remove a lot of ongoing hassles. Without a separate database, cache, or queue, there is less network traffic (because the SQLite file is local), and less servers to manage, maintain, and backup.

## Some mild concerns

It's not all gravy, though. There are a few things to watch out for when using SQLite in production.

### One container to rule them all

Because the SQLite file is typically local to the container, it is not straight-forward to have multiple containers share the same database. Usually that will not be a problem for low to medium traffic sites because they might not need to scale horizontally beyond a single container. Increasing the number of worker processes in `gunicorn` (or other webservers) and/or increasing the amount of CPUs available to the container can mitigate this restriction.

There are also a few other options that attempt to scale SQLite across multiple hosts. I have not investigted any of these fully, but wanted to mention them just in case.

- [SQLite Cloud](https://sqlitecloud.io/): Cloud-based SQLite database service ([Django quick start](https://docs.sqlitecloud.io/docs/quick-start-django))
- [Turso libSQL](https://turso.tech/libsql): A fork of SQLite that supports distributed databases ([django-libsql](https://github.com/profusion/django_libsql))
- [rqlite](https://rqlite.io/): The lightweight, user-friendly, distributed relational database built on SQLite
- [marmot](https://github.com/maxpert/marmot): A distributed SQLite replicator built on top of NATS

### Deployment downtime

Because of the "only one host" issue, no-downtime deployment is a little tricky. I detail an approach for limited downtime during deployment below using [Litestream](https://litestream.io/) to replicate/restore the database, which seems like an acceptable trade-off for many projects.

## Django settings

Django has great initial support for SQLite and, with a few tweaks, it can serve production traffic for the database, cache, and queue broker.

### Database

Django has [built-in support for SQLite](https://docs.djangoproject.com/en/stable/ref/databases/#sqlite-notes) and the default `settings.py` uses SQLite, so you have probably seen something like this before.

```python
# settings.py

...

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}
```

These settings will work okay for local development, but they are not optimal for production. When running under any sort of load you will run into the dreaded [database is locked](https://blog.pecar.me/django-sqlite-dblock) error. To prevent this issue, change the `"default"` database to include the following options which are based on best practices from Rails. I also tend to put the database in a separate directory (configured with the `"NAME"` key) called "db" to keep the root directory clean.

>The settings below are only applicable in Django 5.1+. If you are running an older version see [Anže's article](https://blog.pecar.me/sqlite-django-config#in-django-50-42-or-older) for another approach.

```python
# settings.py

...

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/site.sqlite3",
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",
            "timeout": 5,  # seconds
            "init_command": """
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                PRAGMA mmap_size=134217728;
                PRAGMA journal_size_limit=27103364;
                PRAGMA cache_size=2000;
            """,
        },
    },
}
```

>You might wonder if the [foreign_keys PRAGMA](https://www.sqlite.org/pragma.html#pragma_foreign_keys) would be useful. Lucky for you, Django [already includes it](https://github.com/django/django/blob/stable/5.1.x/django/db/backends/sqlite3/base.py#L203) for SQLite databases!

### Cache

Django has a [built-in database cache](https://docs.djangoproject.com/en/stable/topics/cache/#database-caching). You can enable it by adding the following to your `settings.py` file.

```python
# settings.py

...

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache",
    }
}
```

However, that will use the `"default"` database configured above. Depending on your needs, you may want to use a separate SQLite database for the cache. I like this approach because I tend to think of cache as ephemeral, therefore I do not want the cache database table to be backed up along with the main database.

#### Update databases settings

```python
# settings.py

...

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/site.sqlite3",
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",
            "timeout": 5,  # seconds
            "init_command": """
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                PRAGMA mmap_size=134217728;
                PRAGMA journal_size_limit=27103364;
                PRAGMA cache_size=2000;
            """,
        },
    },
    "cache": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/cache.sqlite3",
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",
            "timeout": 5,  # seconds
            "init_command": """
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                PRAGMA mmap_size=134217728;
                PRAGMA journal_size_limit=27103364;
                PRAGMA cache_size=2000;
            """,
        },
    },
}
```

#### Add a cache database router

Because the cache database is separate from the `"default"` database, we need to tell Django about it with a [database router](https://docs.djangoproject.com/en/stable/topics/db/multi-db/#database-routers).

Create a new file called `routers.py` and add the following to it. I put it in a directory named "project", but it can go anywhere.

```python
# routers.py

DJANGO_CACHE_APP_LABEL = "django_cache"


class CacheRouter:
    """Route cache queries to a separate "cache" database."""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == DJANGO_CACHE_APP_LABEL:
            return "cache"

        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == DJANGO_CACHE_APP_LABEL:
            return "cache"

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == DJANGO_CACHE_APP_LABEL:
            return db == "cache"

        return None
```

Then add the following to `settings.py`.

```python
# settings.py

...

DATABASE_ROUTERS = ["project.database_routers.CacheRouter"]
```

#### Cache table creation

You will need to call [createcachetable](https://docs.djangoproject.com/en/5.1/ref/django-admin/#django-admin-createcachetable) as part of the deployment process to create the cache table like the following.

```bash
python manage.py createcachetable --database cache
```

### Queue

In the past, there were specific services like `RabbitMQ` that were used for queueing tasks. However, there are a few Django libraries that can use the database (and by extension SQLite) to queue background jobs.

- [django-q2](https://github.com/django-q2/django-q2)
- [django-db-queue](https://github.com/dabapps/django-db-queue)
- [huey](https://huey.readthedocs.io)

## Deployments

As mentioned above, because SQLite is just a file in the same container as the webserver, when a new container spins up with a deployment, the current state of the database will be lost.

Thankfully, there are a few approaches to handle this. One is to replicate the continually current database state to an S3 bucket and then restore it during new deployments.

The basic idea is:

1. Replicate the current state of the database to an S3 bucket while container 1 is serving traffic
2. When a new deployment starts, spin up container 2
3. Container 2 downloads the current state of the database from the S3 bucket
4. Switch traffic from container 1 to container 2
5. Container 2 starts serving traffic and replicating the database to the S3
6. Container 1 shuts down

With something like [Coolify](https://coolify.io/), the switch from container 1 to container 2 will be handled automatically for you. There will be a _slight_ blip during deployments, but it will be very minimal -- that's the trade-off for less complexity and a simpler infrastructure setup. And with a CDN like Cloudflare or Fastly serving the website, the downtime potentially can be non-existent.

[Litestream](https://litestream.io/) is the gold standard for replicating SQLite databases to S3. There are many S3-compatible storage options available. I currently ship a replica to both [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/) _and_ [Hetzner Object Storage](https://www.hetzner.com/storage/object-storage/) just in case. [Backblaze B2](https://www.backblaze.com/cloud-storage) is another option, as is [AWS S3](https://aws.amazon.com/s3/), obviously.

First, I install `Litestream` as part of my `Dockerfile`.

```Dockerfile
...

# Install wget and Litestream
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update --fix-missing && \
    apt-get install --no-install-recommends -y wget && \
    wget https://github.com/benbjohnson/litestream/releases/download/v0.3.13/litestream-v0.3.13-linux-amd64.deb && \
    dpkg -i litestream-v0.3.13-linux-amd64.deb

ENTRYPOINT ["./entrypoint.sh"]
```

Then, in the `entrypoint.sh` file, I add the following to restore the database from S3, collect static assets, migrate the database, create the cache table, and finally, start the webserver.

```bash
#!/bin/sh
set -eux

echo "Setup database..."
mkdir -p "db"
chmod -R a+rwX "db"
litestream restore -config litestream.yml -if-db-not-exists -if-replica-exists "db/site.sqlite"

echo "Collect static files..."
python manage.py collectstatic --noinput

echo "Migrate databases..."
python manage.py migrate --noinput

echo "Create cache table..."
python manage.py createcachetable --database cache

echo "Start litestream and gunicorn..."
litestream replicate -config litestream.yml -exec "gunicorn project.wsgi --config=gunicorn.conf.py"
```

>The `-exec` argument for [`replicate`](https://litestream.io/reference/replicate/) starts the `gunicorn` process and allows `litestream` to do simple process management for the webserver.

In the `litestream.yml` file, I have the following [configuration](https://litestream.io/reference/config/).

```yaml
dbs:
  - path: db/site.sqlite3
    replicas:
      - name: my_s3
        type: s3
        endpoint: s3-endpoint.com
        access-key-id: ACCESS_KEY_ID
        secret-access-key: SECRET_ACCESS_KEY
        bucket:   bucket-name
        path:     site/site.sqlite3
```

>The `access-key-id` and `secret-access-key` can be read from environment variables to prevent checking in secrets to version control.

## Conclusion

With the above setup we have accomplished a few things:

- Reduced complexity: no separate servers for database, cache, or queue broker
- Reduced network latency: the SQLite file is local to the container so there are no network hops
- Lower cost: no managed servers to pay for
- Less maintenance: less servers to manage, keep up to date, and backup

Hopefully this was helpful if you are looking to use SQLite with Django in production. Please reach out to me on [Mastodon](https://indieweb.social/@adamghill) or [Bluesky](https://bsky.app/profile/adamghill.com) if you have any questions or feedback!

## More resources, documentation, and details

- [Litestream](https://litestream.io)
- [blaze-starter start.sh](https://github.com/piepworks/blaze-starter/blob/main/start.sh)
- [Django, SQLite, and the Database is Locked Error](https://blog.pecar.me/django-sqlite-dblock)
- [Django SQLite Production Config](https://blog.pecar.me/sqlite-django-config)
- [Gotchas with SQLite in Production](https://blog.pecar.me/sqlite-prod)
- [Django SQLite Benchmark](https://blog.pecar.me/django-sqlite-benchmark)
- [Django SQLite foreign_keys pragma](https://github.com/django/django/blob/stable/5.1.x/django/db/backends/sqlite3/base.py#L203)
- [Why Litestack?](https://github.com/oldmoe/litestack/blob/master/WHYLITESTACK.md)
- [Consider SQLite](https://blog.wesleyac.com/posts/consider-sqlite)
- [Ask HN: Are you using SQLite and Litestream in production?](https://news.ycombinator.com/item?id=39065201)

> Thank you to [Tim White](https://fosstodon.org/@timlwhite) and [Sangeeta Jadoonanan](https://fosstodon.org/@sjbitcode) for proof-reading this article.

> Photo by <a href="https://unsplash.com/@jankolar?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Jan Antonin Kolar</a> on <a href="https://unsplash.com/photos/brown-wooden-drawer-lRoX0shwjUQ?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
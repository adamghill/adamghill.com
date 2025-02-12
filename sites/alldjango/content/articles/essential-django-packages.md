---
template: base.html
title: Essential Django packages ❤️
date: 2025-01-12 20:22:16 -0500
categories: django python
description: Libraries that I always use with Django.
---

Django is sometimes called the batteries-included web framework, but there are a few third-party packages I tend to install for every Django project. I have categorized the packages for different use-cases, although one important note is that I am primarily thinking about side projects and websites with reasonable traffic requirements (i.e. 99% of the websites ever created). I personally have a few sites that have survived the Hacker News home page with most of this stack, so you'll also probably be just fine (and it turns out that judicious use of caching with `redis` can handle _a lot_ of traffic). 😉

Thanks to Will Vincent for publishing [20 Django Packages That I Use in Every Project](https://learndjango.com/tutorials/20-django-packages-i-use-every-project) which directly inspired this post -- we have a few packages which overlap, but of course there are some differences. Also, if you need more awesomeness there is always [awesomedjango.org](https://awesomedjango.org) or... if you want to see the whole breadth of options check out [djangopackages.org](https://djangopackages.org)!

I have tried to include links to the project sponsor/donation page if I could find it (please let me know if I missed any). One way to support the libraries you use is by donating/sponsoring them. Or better yet, get your workplace to sponsor the open source software they rely on!

And finally, just a note: lists like this are inherently subjective -- all libraries have their own trade-offs and nothing is perfect for everyone. I built up this list by trying lots of libraries  and seeing what worked for me and what _I_ liked. I humbly suggest you come up with your own list, write it up, and let me know on [Mastodon](https://indieweb.social/@adamghill) or [Bluesky](https://bsky.app/profile/adamghill.com) -- I'd love to hear what packages I'm missing out on!

>Last updated on January 12th, 2025.


## Python-related

### [uv](https://docs.astral.sh/uv/)

I was a big proponent of the `Poetry` package manager for a while, but have started switching more and more projects to `uv`. They are somewhat similar, but `uv` tends to follow standard PEPs a little more closely and has that magical Astral speed.

### [ruff](https://docs.astral.sh/ruff/)

Maybe 8 years ago a co-worker tried to convince me to use `yapf` and I was dead-set against it. I probably said something like, "Why would I want something to change my code automatically?!" or "I don't agree with this one formatting rule, therefore it must be bad."

Yikes. My opinion has completely changed. At first, `isort` opened my eyes to the wonder of not manually alphabetizing all of my code imports. Then, `black` came along (with its delightful lack of settings) and I realized that I was willing to trade "my personal code style" for "never thinking about code formatting ever again". _Especially_ when working in a team where everyone tends to have their own "style".

Then, `ruff` was released and eventually replaced `flake8`, `black`, _and_ `isort` with its lightning fast speed.

### [pytest-django](https://pytest-django.readthedocs.io/)

I appreciate that Django has unit testing built-in. However, I do not tend to use it because I have completely converted to the church of `pytest`. The lack of required classes is appealing and fixtures are wonderful (even if they are _sometimes_ a little too magical 🪄). I appreciate the fine-grained control over the database, especially [preventing migrations from running](https://pytest-django.readthedocs.io/en/latest/database.html#no-migrations-disable-django-migrations) and all of the [Django-specific fixtures](https://pytest-django.readthedocs.io/en/latest/helpers.html#fixtures).

### [pytest-cov](https://pytest-cov.readthedocs.io/)

Integrates `pytest` with `coverage` to tell you how much of your code is covered by unit tests. Very straight-forward and useful. I tend to have a separate command for generating coverage reports so it doesn't slow down the red/green/refactor test cycle.


## Core Django

If I could wave a magic wand, I wish at least a little bit of the functionality of these packages would be incorporated into Django. I (helpfully?) rant about making Django more "batteries-included" in [Django Roadmap 2024](https://dev.to/adamghill/django-roadmap-2024-2ocn#modernize).

### [python-dotenv](https://saurabh-kumar.com/python-dotenv/)

I tend to reach for `python-dotenv` although `django-environs` is also great. There are a bunch of similar libraries available, but all I need is a way to load an `.env` file into Django settings to follow the [twelve-factor](https://12factor.net/config) approach and keep secrets out of my code.

### [django-cache-memoize](https://django-cache-memoize.readthedocs.io/)

This is a function decorator that integrates with the core Django cache. There are a lot of cache decorator libraries floating around, but I have run into a few gotchas with them. `django-cache-memoize` works exactly as expected.

### [django-model-utils](https://django-model-utils.readthedocs.io/)

[Sponsor django-model-utils](https://jazzband.co/donate) ❤️

This is very silly, but I literally install this package for one particular model mixin: [`TimeStampedModel`](https://django-model-utils.readthedocs.io/en/latest/models.html#timestampedmodel). I use it _everywhere_ -- basically any model that might be useful to know when it got last updated. Insanely useful for lightweight audit tracking of a model.

### [whitenoise](https://whitenoise.readthedocs.io/)

Stop messing with S3 buckets and the atrocious AWS console. `whitenoise` will set the correct cache headers on your static assets automagically and a CDN like Cloudflare or Fastly will serve your assets without ever hitting your Django app. Even without a CDN, NGINX can serve static assets to greatly reduce the amount of load on your WSGI server.


## Server-side rendering

### [django-tailwind-cli](https://django-tailwind-cli.readthedocs.io)

Since I'm not a designer, I tend to like frameworks like `Bulma` and `Bootstrap` (or even classless CSS like [`Marx`](https://mblode.github.io/marx/) and [`SimpleCSS`](https://simplecss.org/)). However, I have been pleasantly surprised with [`DaisyUI`](https://daisyui.com/) which is basically a layer of semantic CSS on top of `Tailwind`. It provides a good starting point for someone like myself and has lots of components that I can customize as needed.

The [`django-tailwind-cli`](https://django-tailwind-cli.readthedocs.io) library makes it very straight-forward to integrate [Tailwind](https://tailwindcss.com/) with Django. It removes the need for a separate `NodeJS` process to build the output CSS.

### [django-compressor](https://django-compressor.readthedocs.io/)

Compress JavaScript or CSS in production with hashed filenames (which breaks the long-term cache when used with `whitenoise`). There are a lot of settings, but I just copy and paste the same configuration into every project now and it works perfectly. Pair it with [`django-libsass`](https://github.com/torchbox/django-libsass) to support SASS files without an extra build step.

### [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks)

[Sponsor django-widget-tweaks](https://jazzband.co/donate) ❤️

Very underrated in my opinion, `django-widget-tweaks` provides a few template tags to help render forms and fields in HTML. Usually when working with designers or more front-end folks, this allows them to customize HTML without touching Python or understanding the form rendering in Django.

### [django-allauth](https://docs.allauth.org/)

[Sponsor pennersr](https://github.com/sponsors/pennersr/) on GitHub ❤️

The premier authentication provider for integrating Django with third-party logins like Google, Facebook, LinkedIn, etc. The number of providers is staggering and always growing. [pennersr](https://github.com/pennersr) does a great job of handling the myriad support requests for such an integral part of the ecosystem. `django-allauth` also has an exciting [roadmap for 2024](https://allauth.org/news/2024/03/ngi-zero-grant-plan/) which makes me hopeful it can continue to solve Django authentication needs far into the future.

### [django-allauth-ui](https://github.com/danihodovic/django-allauth-ui)

If your site uses `django-allauth` and `Tailwind`, `django-allauth-ui` provides a nicely themed UI for account functionality like login and registration pages.

## API

Django is frequently used just as an API and paired with a frontend framework these days. These are some libraries that I have used to provide APIs in my Django projects.

### [django-ninja](https://django-ninja.dev)

[Sponsor django-ninja](https://www.buymeacoffee.com/djangoninja) on BuyMeACoffee ☕️

`django-rest-framework` is the 800-pound gorilla when building a REST framework with Django. It has a lot of documentation and lots of supporters. Personally, I also find it a little cumbersome to use and grok. I have only used `django-ninja` for a few projects, but I really enjoyed its approach, especially if you have ever used `FastAPI` or are a fan of Python typing. Looking forward to it continuing to evolve!

### [strawberry](https://strawberry.rocks/docs/integrations/django)

[Sponsor strawberry-graphql](https://github.com/sponsors/strawberry-graphql) on GitHub ❤️

Similar to `django-ninja`, `strawberry` uses Python types to provide a GraphQL interface. I have also only used it for a few projects, but I was very happy with the developer experience (especially compared to Apollo).


## Background tasks

### [django-q2](https://django-q2.readthedocs.io/)

I have tried `celery`, `django-rq`, and `huey` and have always returned back to `django-q2` when I need a background task runner for long-running tasks. My favorite features are the integration with Django admin, the ability to use either `redis` or a database to store tasks, and the cron-like scheduler.


## Running in production

These are packages that I always use on production. They are all battle-tested, stable, fast, and [boring technology](https://boringtechnology.club) (in the best possible sense of the phrase).

### [gunicorn](https://gunicorn.org)

My go-to WSGI server for production. Extremely stable and when paired with NGINX for static assets it can handle a decent amount of traffic. I have seen benchmarks that other servers might be faster, but `gunicorn` is rock-solid and configuration is simple -- exactly what I'm looking for.

### [Psycopg 2](https://www.psycopg.org/docs/)

[Sponsor dvarrazzo](https://github.com/sponsors/dvarrazzo?o=esb) on GitHub ❤️

Django has support for other relational databases, but I switched from MySQL to PostgreSQL a long time ago and never looked back. However, I wouldn't ever want to operate any database in production (especially not PostgreSQL!). I suggest finding a cloud provider who has a managed PostgreSQL offering. It's worth it.

[Psycopg 3](https://www.psycopg.org/psycopg3/docs/) is now released, but I have not used it in production... yet.

### [redis](https://pypi.org/project/redis/) + [hiredis](https://pypi.org/project/hiredis/)

`redis` is fast, it's got minimal resource requirements, and it's my go-to cache. As opposed to PostgreSQL I do run my own `redis` in production because I treat the data as ephemeral. If my lack of DevOps-fu breaks it, it shouldn't matter.

Note: as of Django 4, support for `redis` cache is included in Django. If you are using a previous version (or need some [more advanced features](https://github.com/jazzband/django-redis/issues/585)), [`django-redis`](https://github.com/jazzband/django-redis) can be installed.

### [Sentry](https://docs.sentry.io/platforms/python/integrations/django/)

Sentry was originally built on top of Django and still has the best error reporting and monitoring I've ever seen for the web framework (although they support a dizzying amount of other frameworks as well).

Unfortunately, the free tier is not all that useful with any sort of traffic. I also tried self-hosting `GlitchTip` for a brief amount of time, but it wasn't worth the effort personally. I have gotten very used to the details available in Sentry and it's challenging for me to troubleshoot production problems without it now!


## Related lists for Django

- Will Vincent's [20 Django Packages That I Use in Every Project](https://learndjango.com/tutorials/20-django-packages-i-use-every-project)

>Big thanks to [Sangeeta Jadoonanan](https://fosstodon.org/@sjbitcode) for proof-reading this article and giving me some ✨super✨ helpful feedback.

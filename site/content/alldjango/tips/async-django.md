---
template: alldjango/base.html
title: Async Django
description: Async Django
tags: django,templatetag
---

The steadily added async support to different layers of the Django stack over the past few releases has been inspiring to watch. With Django 4.1, async support was added to the ORM and with 4.2 async support was added to Django `Model`s. Both additions are particularly useful with [`django-ninja`](https://django-ninja.rest-framework.com/) which melds a `FastAPI`-like API development experience with the rock-solid benefits of Django.

https://docs.djangoproject.com/en/latest/topics/async/ has the latest state of asynchronous support in Django.

https://fly.io/django-beats/running-tasks-concurrently-in-django-asynchronous-views/ has a good overview of the history and how to use an async view to call two methods at once.

However, there are still a few sticking gotchas when writing async views with Django.

## Async views calling async functions

Let's say you have a `Book` model with an async model method.

```python
import httpx

class Book(models.Model):
    title = models.CharField(max_length=255)

    async def get_(self):
        httpx.get("https://some-book-title-lookup.com")
```

```python
from typing import Awaitable, Callable

from asgiref.sync import async_to_sync
from django import template

register = template.Library()


@register.filter
def syncify(fn):
    @async_to_sync()
    def _syncify(fn: Awaitable) -> Callable:
        return fn

    return _syncify(fn)
```

```html
dslfkj
```
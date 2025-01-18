---
template: base.html
title: Curated Django libraries
tags: django,python
draft: true
---

I think of building websites as a sort of _Choose Your Own Adventure_ where you get to make decisions based on what the end goal is. Personally, I am not normally building complete "web applications" like Gmail so I tend to focus on simplicity and reducing the number of different paradigms I have to deal with. Along with that, I try to choose libraries that are well-maintained and have good documentation. So, this is a _curated_ list of libraries that I have found useful to build the types of websites that I tend to build.

This list is ever-changing, but I will try to keep it updated over time (last updated January 12th, 2025).

Note that this list might be different than what you use. That's ok! I feel like technology choices can be surprisingly subjective, but hopefully this list is a good place to start if you are looking for ideas.

## Web Frameworks

### Full-featured

My default web framework is [`Django`](https://www.djangoproject.com/) (no surprise considering the domain of this website!). By full-featured I mean things like:

- database access with an ORM
- authentication
- cache
- built-in admin UI

### Content site

If I don't need an entire web application, but want something closer to a static site I use my own `Coltrane` framework. It uses `Django` under the hood, but reduces a lot of the decision points and automatically converts Markdown files to HTML (fun fact: this site is made with `Coltrane`!)

## JavaScript

Honestly, vanilla JavaScript isn't too bad these days. However, [`HTMX`](https://htmx.org/) fits in nicely with `Django` for most of the interactive functionality I need. The [`django-htmx`](https://django-htmx.readthedocs.io) library also provides useful functionality.

## CSS

### Full-featured

`Tailwind` can be a little divisive and I, personally, bristle at the overwhelming amount of classes required to render a decent looking UI. Since I am not a designer, I also like for a framework to provide a good starting point. I have been pleasantly surprised with [`DaisyUI`](https://daisyui.com/) which provides a layer of semantic CSS on top of `Tailwind`. It provides a good starting point with a lot of components that are very easy to customize by adding `Tailwind` classes as needed.

The [`django-tailwind-cli`](https://django-tailwind-cli.readthedocs.io) library makes it more straight-forward to use [Tailwind](https://tailwindcss.com/) with `Django`. It removes the need for a separate `NodeJS` process to build the CSS by wrapping the normal `Django` `runserver` management command. Highly recommended!

### Classless

For simple sites where I don't want (or need!) a lot of functionality, I tend to use classless CSS frameworks. They are usually smaller in size than a more full-featured CSS framework, and good for prototypes and basic websites.

[`Marx`](https://mblode.github.io/marx/) and [`SimpleCSS`](https://simplecss.org/) are classless CSS stylesheets I have used in the past -- both work well!

## Features

### Authentication

`Django` has a built-in authentication system, but [`django-allauth`](https://docs.allauth.org) provides a lot of features on top, including account templates, social logins, double opt-in registration, multi-factor authentication, etc.

And if your site uses `Tailwind`, [`django-allauth-ui`](https://github.com/danihodovic/django-allauth-ui) can be installed to provide a nicely themed UI for logging in and registering.

### Queues

Queues can be utilized for background tasks like sending emails, hitting external APIs, running scheduled tasks, etc. Offloading work to a queue is a great way to improve a user's experience with your website.

[`django-q2`](https://django-q2.readthedocs.io) provides a straight-forward way to run background tasks. It also provides a built-in scheduler to run tasks at regular intervals.

### Static Assets

[`whitenoise`](https://whitenoise.readthedocs.io) sets appropriate cache headers on static assets, so that they can be served without hitting your `Django` app. Using `whitenoise` along with a CDN like Cloudflare and Fastly can greatly improve the responsiveness of your site.

[`django-compressor`](https://django-compressor.readthedocs.io) compresses static assets like JavaScript and CSS. It can even process the contents of SASS files with [`django-libsass`](https://github.com/torchbox/django-libsass).

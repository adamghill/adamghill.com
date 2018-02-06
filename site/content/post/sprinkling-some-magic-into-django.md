---
title: Sprinkling some Magic into Django
date: 2018-02-06T20:58:19.386Z
description: >-
  I (mostly) love Python and I have a lot of experience building sites in
  Django, so it is my go-to framework. The database ORM, request, response and
  templating fundamentals of Django are rock-solid, however, using it with a
  more modern JavaScript framework does not always feel as seamless. The work
  being done in for channels is intriguing, but fundamentally Django is a
  server-side webstack. I was having a hard time finding best practices for
  using the best of Django for its strengths, but also create the interactive
  experience that users expect in a modern web application.
---
If you are creating a site from scratch, then using Django REST Framework to provide an API and building a SPA on top is one way to approach the solution. I already had a (large) existing website and can quickly add new models, routes and templates for new functionality. I was looking for an easy way to sustainably add AJAX to my existing Django site. I was using jQuery for a few bits of interactivity, and had used VueJS for a prototype page, but I found myself re-inventing the wheel.

`djajax` is my attempt to sprinkle some AJAX into a Django site without throwing out all of the benefits of Django. Currently, it consists of a model mixin to serialize a model or queryset (including pagination) to JSON objects. Template filters and tags to convert a dictionary template variable into JSON, and a way to cleanly expose routes with url reversing. It also contains view functions to drop into an existing view function and make it "AJAX-aware". This includes a some helper methods for POSTing from the client and automatically handling model creates/updates/deletes.

One nice benefit of using the existing (either function or class-based) views is that authentication and authorization is exactly the same as server-side. It also lets you build out functionality in the standard Django way, and quickly add AJAX functionality as needed.

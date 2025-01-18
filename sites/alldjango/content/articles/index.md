---
template: base.html
title: Articles
description: A list of all articles.
---

{% directory_contents 'articles' order_by="-date" as articles %}
{% include '_contents.html' with contents=articles %}

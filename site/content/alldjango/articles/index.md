---
template: alldjango/base.html
title: Articles
description: A list of all articles.
---

{% directory_contents 'alldjango/articles' order_by="-date" as articles %}
{% include 'alldjango/_contents.html' with contents=articles %}

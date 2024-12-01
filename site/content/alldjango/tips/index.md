---
template: alldjango/base.html
title: Tips
description: A list of all tips.
---

{% directory_contents 'alldjango/tips' order_by="-date" as tips %}
{% include 'alldjango/_contents.html' with contents=tips %}

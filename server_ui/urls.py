# -*- coding: utf-8 -*-
from django.urls import re_path

from .views import home, about, docs, faq, privacy

urlpatterns = [
    re_path(r"^$", home),
    re_path(r"^about$", about),
    re_path(r"^docs$", docs),
    re_path(r"^faq$", faq),
    re_path(r"^privacy$", privacy),
]

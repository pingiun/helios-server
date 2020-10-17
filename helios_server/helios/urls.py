# -*- coding: utf-8 -*-
from django.conf.urls import include
from django.urls import re_path

from . import url_names as names
from . import views

urlpatterns = [
    re_path(r"^autologin$", views.admin_autologin),
    re_path(r"^testcookie$", views.test_cookie, name=names.COOKIE_TEST),
    re_path(r"^testcookie_2$", views.test_cookie_2, name=names.COOKIE_TEST_2),
    re_path(r"^nocookies$", views.nocookies, name=names.COOKIE_NO),
    re_path(r"^stats/", include("helios_server.helios.stats_urls")),
    # election shortcut by shortname
    re_path(
        r"^e/(?P<election_short_name>[^/]+)$",
        views.election_shortcut,
        name=names.ELECTION_SHORTCUT,
    ),
    re_path(
        r"^e/(?P<election_short_name>[^/]+)/vote$",
        views.election_vote_shortcut,
        name=names.ELECTION_SHORTCUT_VOTE,
    ),
    # vote shortcut
    re_path(
        r"^v/(?P<vote_tinyhash>[^/]+)$",
        views.castvote_shortcut,
        name=names.CAST_VOTE_SHORTCUT,
    ),
    # trustee login
    re_path(
        r"^t/(?P<election_short_name>[^/]+)/(?P<trustee_email>[^/]+)/(?P<trustee_secret>[^/]+)$",
        views.trustee_login,
        name=names.TRUSTEE_LOGIN,
    ),
    # election
    re_path(r"^elections/params$", views.election_params, name=names.ELECTIONS_PARAMS),
    re_path(
        r"^elections/verifier$", views.election_verifier, name=names.ELECTIONS_VERIFIER
    ),
    re_path(
        r"^elections/single_ballot_verifier$",
        views.election_single_ballot_verifier,
        name=names.ELECTIONS_VERIFIER_SINGLE_BALLOT,
    ),
    re_path(r"^elections/new$", views.election_new, name=names.ELECTIONS_NEW),
    re_path(
        r"^elections/administered$",
        views.elections_administered,
        name=names.ELECTIONS_ADMINISTERED,
    ),
    re_path(r"^elections/voted$", views.elections_voted, name=names.ELECTIONS_VOTED),
    re_path(
        r"^elections/(?P<election_uuid>[^/]+)",
        include("helios_server.helios.election_urls"),
    ),
]

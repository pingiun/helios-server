# -*- coding: utf-8 -*-
from django.conf.urls import include
from django.urls import re_path

<<<<<<< HEAD
from . import views, url_names as names

urlpatterns = [
    url(r"^autologin$", views.admin_autologin),
    url(r"^testcookie$", views.test_cookie, name=names.COOKIE_TEST),
    url(r"^testcookie_2$", views.test_cookie_2, name=names.COOKIE_TEST_2),
    url(r"^nocookies$", views.nocookies, name=names.COOKIE_NO),
    url(r"^stats/", include("helios.stats_urls")),
    # election shortcut by shortname
    url(
=======
import helios.url_names as names
from helios import views

urlpatterns = [
    re_path(r"^autologin$", views.admin_autologin),
    re_path(r"^testcookie$", views.test_cookie, name=names.COOKIE_TEST),
    re_path(r"^testcookie_2$", views.test_cookie_2, name=names.COOKIE_TEST_2),
    re_path(r"^nocookies$", views.nocookies, name=names.COOKIE_NO),
    re_path(r"^stats/", include("helios.stats_urls")),
    # election shortcut by shortname
    re_path(
>>>>>>> adf4978... Update for python 3.9
        r"^e/(?P<election_short_name>[^/]+)$",
        views.election_shortcut,
        name=names.ELECTION_SHORTCUT,
    ),
<<<<<<< HEAD
    url(
=======
    re_path(
>>>>>>> adf4978... Update for python 3.9
        r"^e/(?P<election_short_name>[^/]+)/vote$",
        views.election_vote_shortcut,
        name=names.ELECTION_SHORTCUT_VOTE,
    ),
    # vote shortcut
<<<<<<< HEAD
    url(
=======
    re_path(
>>>>>>> adf4978... Update for python 3.9
        r"^v/(?P<vote_tinyhash>[^/]+)$",
        views.castvote_shortcut,
        name=names.CAST_VOTE_SHORTCUT,
    ),
    # trustee login
<<<<<<< HEAD
    url(
=======
    re_path(
>>>>>>> adf4978... Update for python 3.9
        r"^t/(?P<election_short_name>[^/]+)/(?P<trustee_email>[^/]+)/(?P<trustee_secret>[^/]+)$",
        views.trustee_login,
        name=names.TRUSTEE_LOGIN,
    ),
    # election
<<<<<<< HEAD
    url(r"^elections/params$", views.election_params, name=names.ELECTIONS_PARAMS),
    url(
        r"^elections/verifier$", views.election_verifier, name=names.ELECTIONS_VERIFIER
    ),
    url(
=======
    re_path(r"^elections/params$", views.election_params, name=names.ELECTIONS_PARAMS),
    re_path(
        r"^elections/verifier$", views.election_verifier, name=names.ELECTIONS_VERIFIER
    ),
    re_path(
>>>>>>> adf4978... Update for python 3.9
        r"^elections/single_ballot_verifier$",
        views.election_single_ballot_verifier,
        name=names.ELECTIONS_VERIFIER_SINGLE_BALLOT,
    ),
<<<<<<< HEAD
    url(r"^elections/new$", views.election_new, name=names.ELECTIONS_NEW),
    url(
=======
    re_path(r"^elections/new$", views.election_new, name=names.ELECTIONS_NEW),
    re_path(
>>>>>>> adf4978... Update for python 3.9
        r"^elections/administered$",
        views.elections_administered,
        name=names.ELECTIONS_ADMINISTERED,
    ),
<<<<<<< HEAD
    url(r"^elections/voted$", views.elections_voted, name=names.ELECTIONS_VOTED),
    url(r"^elections/(?P<election_uuid>[^/]+)", include("helios.election_urls")),
=======
    re_path(r"^elections/voted$", views.elections_voted, name=names.ELECTIONS_VOTED),
    re_path(r"^elections/(?P<election_uuid>[^/]+)", include("helios.election_urls")),
>>>>>>> adf4978... Update for python 3.9
]

"""
Helios URLs for Election related stuff

Ben Adida (ben@adida.net)
"""

from django.urls import re_path

from .stats_views import (
    home,
    force_queue,
    elections,
    recent_problem_elections,
    recent_votes,
)
from . import stats_url_names as names

urlpatterns = [
    re_path(r"^$", home, name=names.STATS_HOME),
    re_path(r"^force-queue$", force_queue, name=names.STATS_FORCE_QUEUE),
    re_path(r"^elections$", elections, name=names.STATS_ELECTIONS),
    re_path(
        r"^problem-elections$",
        recent_problem_elections,
        name=names.STATS_ELECTIONS_PROBLEMS,
    ),
    re_path(r"^recent-votes$", recent_votes, name=names.STATS_RECENT_VOTES),
]

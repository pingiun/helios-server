from django.conf import settings
from django.conf.urls import include
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    re_path(r"^auth/", include("helios_server.helios_auth.urls")),
    re_path(r"^helios/", include("helios_server.helios.urls")),
    # SHOULD BE REPLACED BY APACHE STATIC PATH
    re_path(
        r"booth/(?P<path>.*)$",
        serve,
        {"document_root": settings.ROOT_PATH + "/heliosbooth"},
    ),
    re_path(
        r"verifier/(?P<path>.*)$",
        serve,
        {"document_root": settings.ROOT_PATH + "/heliosverifier"},
    ),
    re_path(
        r"static/auth/(?P<path>.*)$",
        serve,
        {"document_root": settings.ROOT_PATH + "/helios_auth/media"},
    ),
    re_path(
        r"static/helios/(?P<path>.*)$",
        serve,
        {"document_root": settings.ROOT_PATH + "/helios/media"},
    ),
    re_path(
        r"static/(?P<path>.*)$",
        serve,
        {"document_root": settings.ROOT_PATH + "/server_ui/media"},
    ),
    re_path(r"^", include("helios_server.server_ui.urls")),
]

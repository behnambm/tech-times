from __future__ import absolute_import

from django.conf.urls import url
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r"^upload/", views.upload, name="ckeditor_upload"),
    url(
        r"^browse/",
        never_cache(login_required(views.browse)),
        name="ckeditor_browse",
    ),
]

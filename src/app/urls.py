from django.urls import re_path
from django.views.static import serve

"""
URL configuration for mimosa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("up/", include("up.urls")),
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]

# NOTE: This should be served by a separate web server or CDN, however we are
# temporarily allowing Django to serve these files, see:
# https://stackoverflow.com/questions/2237418/serving-static-media-during-django-development-why-not-media-root
MEDIA_URL_STRIPPED = settings.MEDIA_URL.lstrip("/")
urlpatterns += [
    re_path(
        r"^{}(?P<path>.*)$".format(MEDIA_URL_STRIPPED),
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]

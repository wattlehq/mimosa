import os

from django import get_version
from django.conf import settings
from django.shortcuts import render


def success(request):
    context = {
        "debug": settings.DEBUG,
        "django_ver": get_version(),
        "python_ver": os.environ["PYTHON_VERSION"],
    }

    return render(request, "pages/success.html", context)

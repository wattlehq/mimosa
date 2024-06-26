from django.conf import settings


def get_site_url():
    port = str(settings.SITE_PORT)
    return settings.SITE_PROTOCOL + settings.SITE_DOMAIN + ":" + port

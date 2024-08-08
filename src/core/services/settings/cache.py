from django.core.cache import cache

from core.constants.settings import SETTINGS_CACHE_TIMEOUT


class SettingsCache:
    SETTINGS_CACHE_KEY = "app_settings"

    @classmethod
    def get(cls):
        settings = cache.get(cls.SETTINGS_CACHE_KEY)
        return settings

    @classmethod
    def invalidate(cls):
        """
        Invalidate the settings cache.
        """
        cache.delete(cls.SETTINGS_CACHE_KEY)

    @classmethod
    def update(cls, settings):
        """
        Update the settings cache with the provided settings object.
        """
        cache.set(
            cls.SETTINGS_CACHE_KEY, settings, timeout=SETTINGS_CACHE_TIMEOUT
        )

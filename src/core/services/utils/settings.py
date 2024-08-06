from django.core.cache import cache

from core.constants.settings import SETTINGS_CACHE_TIMEOUT


class SettingsCacheService:
    SETTINGS_CACHE_KEY = "app_settings"

    @classmethod
    def get_settings(cls):
        """
        Retrieve the Settings object from the database or cache.
        Returns:
            Settings: The Settings object.
        Raises:
            ValueError: If no Settings object is found in the database.
        """
        from core.models.settings import (
            Settings,  # Import here to avoid circular import
        )

        settings = cache.get(cls.SETTINGS_CACHE_KEY)
        if not settings:
            settings = Settings.objects.first()
            if not settings:
                raise ValueError("Settings object not found")
            cls.update_settings_cache(settings)
        return settings

    @classmethod
    def invalidate_settings_cache(cls):
        """
        Invalidate the settings cache.
        """
        cache.delete(cls.SETTINGS_CACHE_KEY)

    @classmethod
    def update_settings_cache(cls, settings):
        """
        Update the settings cache with the provided settings object.
        """
        cache.set(
            cls.SETTINGS_CACHE_KEY, settings, timeout=SETTINGS_CACHE_TIMEOUT
        )

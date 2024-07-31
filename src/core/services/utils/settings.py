from django.core.cache import cache

from core.models.settings import Settings


def get_settings():
    """
    Retrieve the Settings object from the database or cache.

    Returns:
        Settings: The Settings object.

    Raises:
        ValueError: If no Settings object is found in the database.
    """
    # Try to get settings from cache first
    settings = cache.get("app_settings")

    if not settings:
        # If not in cache, retrieve from database
        settings = Settings.objects.first()

        if not settings:
            raise ValueError("Settings object not found")

        # Cache the settings for future use (cache for 1 hour)
        cache.set("app_settings", settings, timeout=3600)

    return settings

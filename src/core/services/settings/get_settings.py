from core.models.settings import Settings
from core.services.settings.cache import SettingsCache


def get_settings():
    """
    Retrieve the Settings object from the database or cache.
    Returns:
        Settings: The Settings object.
    Raises:
        ValueError: If no Settings object is found in the database.
    """
    settings = SettingsCache.get()
    if not settings:
        settings = Settings.objects.first()
        if not settings:
            raise ValueError("Settings object not found")
        SettingsCache.update(settings)
    return settings

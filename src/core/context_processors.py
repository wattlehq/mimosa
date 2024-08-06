from core.models.settings import Settings


def settings(request):
    return {"settings": Settings.objects.first()}

from django import forms

from core.models.settings import Settings


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ["logo", "council_email"]

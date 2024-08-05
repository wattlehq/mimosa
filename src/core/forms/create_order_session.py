from django import forms
from core.models.property import Property

class CreateOrderSessionForm(forms.Form):
    property_id = forms.IntegerField()
    lines = forms.JSONField()

    def clean_property_id(self):
        property_id = self.cleaned_data['property_id']
        try:
            Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise forms.ValidationError("Invalid property ID")
        return property_id

    def clean_lines(self):
        lines = self.cleaned_data['lines']
        if not isinstance(lines, list):
            raise forms.ValidationError("Lines must be a list")
        for line in lines:
            if not isinstance(line, dict) or 'certificate_id' not in line:
                raise forms.ValidationError("Each line must be a dictionary with a certificate_id")
        return lines

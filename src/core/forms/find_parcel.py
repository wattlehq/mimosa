from django import forms


class FindParcelForm(forms.Form):
    """Form for searching properties by lot, section, deposited plan, or street address."""

    lot = forms.CharField(max_length=50, required=False)
    section = forms.CharField(max_length=50, required=False)
    deposited_plan = forms.CharField(max_length=50, required=False)
    street_address = forms.CharField(max_length=100, required=False)

    def clean(self):
        """
        Validate that at least one search criterion is provided.

        Returns:
            dict: Cleaned form data.

        Raises:
            forms.ValidationError: If no search criteria are provided.
        """
        cleaned_data = super().clean()
        lot = cleaned_data.get('lot')
        section = cleaned_data.get('section')
        deposited_plan = cleaned_data.get('deposited_plan')
        street_address = cleaned_data.get('street_address')

        if not any([lot, section, deposited_plan]) and not street_address:
            raise forms.ValidationError(
                "Please provide either Lot/Section/Deposited Plan information "
                "or a Street Address."
            )

        return cleaned_data
from django import forms


class FindParcelForm(forms.Form):
    """
    Form for searching properties by
    lot, deposited plan, or street address.
    """

    lot = forms.CharField(max_length=50, required=False)
    section = forms.CharField(max_length=50, required=False)
    deposited_plan = forms.CharField(max_length=50, required=False)
    street_address = forms.CharField(max_length=100, required=False)

    def clean(self):
        """
        Validate that the combination of provided fields
        meets the specified rules.

        Returns:
            dict: Cleaned form data.

        Raises:
            forms.ValidationError: If the combination of fields is not valid.
        """
        cleaned_data = super().clean()
        lot = cleaned_data.get('lot')
        section = cleaned_data.get('section')
        deposited_plan = cleaned_data.get('deposited_plan')
        street_address = cleaned_data.get('street_address')

        if not any([lot, section, deposited_plan, street_address]):
            raise forms.ValidationError(
                "Please provide either a Street Address, or Lot and DP."
                )

        if street_address:
            if lot or section or deposited_plan:
                raise forms.ValidationError(
                    "Street Address should be provided alone, not with Lot, " +
                    "Section, or DP."
                    )
        else:
            if section and not (lot and deposited_plan):
                if lot:
                    raise forms.ValidationError(
                        "Section and Lot provided. Please also include the" +
                        "Deposited Plan."
                        )
                elif deposited_plan:
                    raise forms.ValidationError(
                        "Section and Deposited Plan provided. Please also" +
                        "include the Lot number."
                        )
                else:
                    raise forms.ValidationError(
                        "Section alone is not sufficient. Please provide" +
                        "Lot and Deposited Plan as well."
                        )
            elif lot and not deposited_plan:
                raise forms.ValidationError(
                    "Lot provided without Deposited Plan. Please include" +
                    "both Lot and Deposited Plan."
                    )
            elif deposited_plan and not lot:
                raise forms.ValidationError(
                    "Deposited Plan provided without Lot. Please include" +
                    "both Lot and Deposited Plan."
                    )

        return cleaned_data

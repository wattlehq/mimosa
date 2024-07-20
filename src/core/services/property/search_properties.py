from django.db.models import Q

from core.models.property import Property


def search_properties(cleaned_data):
    """
    Search for properties based on the provided criteria.

    Args:
        cleaned_data (dict): Cleaned form data containing search criteria.

    Returns:
        QuerySet: Filtered Property objects.
    """
    q_objects = Q()

    lot = cleaned_data.get("lot")
    section = cleaned_data.get("section")
    deposited_plan = cleaned_data.get("deposited_plan")
    street_address = cleaned_data.get("street_address")

    if lot or section or deposited_plan:
        if lot:
            q_objects &= Q(lot__icontains=lot)
        if section:
            q_objects &= Q(section__icontains=section)
        if deposited_plan:
            q_objects &= Q(deposited_plan__icontains=deposited_plan)
    elif street_address:
        parts = street_address.split()
        for part in parts:
            q_objects |= (
                Q(address_street__icontains=part)
                | Q(address_suburb__icontains=part)
                | Q(address_state__icontains=part)
                | Q(address_post_code__icontains=part)
            )

    return Property.objects.filter(q_objects)

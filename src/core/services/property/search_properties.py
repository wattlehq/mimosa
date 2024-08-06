from django.db.models import Q

from core.models.property import Property


def search_properties(
    lot=None, section=None, deposited_plan=None, street_address=None
):
    """
    Search for properties based on the provided criteria.

    Args:
        lot (str, optional): Lot number to search for.
        section (str, optional): Section number to search for.
        deposited_plan (str, optional): Deposited plan number to search for.
        street_address (str, optional): Street address to search for.

    Returns:
        QuerySet: Filtered Property objects.
    """
    q_objects = Q()

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

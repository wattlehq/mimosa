from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from core.services.property.serialize_property import serialize_property
from core.services.property.search_properties import search_properties
from core.services.property.group_properties_by_assessment import (
    group_properties_by_assessment,
    )


@require_http_methods(["GET"])
def search_properties_view(request):
    lot = request.GET.get('lot')
    section = request.GET.get('section')
    deposited_plan = request.GET.get('deposited_plan')
    street_address = request.GET.get('street_address')

    properties = search_properties(
        lot,
        section,
        deposited_plan,
        street_address
        )
    grouped_properties = group_properties_by_assessment(properties)

    serialized_grouped_properties = {
        assessment: [serialize_property(prop) for prop in props]
        for assessment, props in grouped_properties.items()
    }

    return JsonResponse(serialized_grouped_properties)

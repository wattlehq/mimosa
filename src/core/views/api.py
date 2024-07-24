from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from core.forms.find_parcel import FindParcelForm
from core.services.property.serialize_property import serialize_property
from core.services.property.search_properties import search_properties
from core.services.property.group_properties_by_assessment import (
    group_properties_by_assessment,
    )


@require_http_methods(["GET"])
def search_properties_view(request):
    """
    View function to handle property search requests.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the serialized
        grouped properties.

    """
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


@require_http_methods(["GET"])
def validate_search_view(request):
    """
    View function to validate search form data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing:
            - isValid (bool): Whether the form data is valid.
            - errors (dict): A dictionary of form errors if any,
                            empty if the form is valid.
    """
    form = FindParcelForm(request.GET)
    is_valid = form.is_valid()

    response_data = {
        "isValid": is_valid,
        "errors": form.errors.get_json_data() if not is_valid else {}
    }

    return JsonResponse(response_data)

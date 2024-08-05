import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from core.forms.find_parcel import FindParcelForm
from core.services.property.serialize_property import serialize_property
from core.services.property.search_properties import search_properties
from core.services.property.group_properties_by_assessment import (
    group_properties_by_assessment,
    )
from core.services.certificate.create_order_session import create_order_session


@require_http_methods(["GET"])
def api_property_search(request):
    """
    View function to validate and handle property search requests.

    Args:
        request (HttpRequest): The HTTP request object containing
        search parameters.

    Returns:
        JsonResponse: A JSON response containing the serialized
        grouped properties or error messages.

    """
    form = FindParcelForm(request.GET)
    if not form.is_valid():
        return JsonResponse({
            "isValid": False,
            "errors": form.errors.get_json_data()
        })

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

    return JsonResponse({
        "isValid": True,
        "results": serialized_grouped_properties
    })

@require_http_methods(["POST"])
def api_create_order_session(request):
    try:
        data = json.loads(request.body)
        result = create_order_session(
            property_id=data['property_id'],
            order_lines=data['lines']
        )
        return JsonResponse(result)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON in request body"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
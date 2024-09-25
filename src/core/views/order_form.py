"""Views for handling property searches and certificate orders."""

from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from core.forms.order.create_order_session import CreateOrderSessionForm
from core.forms.order.find_parcel import FindParcelForm
from core.models.certificate import Certificate
from core.models.property import Property
from core.services.certificate.group_items import group_items_by_parent
from core.services.order.create_order_session import create_order_session
from core.services.property.serialize_property import serialize_property


class OrderForm(View):
    """
    View for handling the find parcel component.

    This view renders the certificate order page and processes
    form submissions for finding parcels.
    """

    template_name = "pages/order_form.html"

    def get(self, request):
        """
        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: Rendered certificate order page with an empty form.
        """
        form_find_parcel = FindParcelForm()
        form_create_order_session = CreateOrderSessionForm()
        certificates = Certificate.objects.all().prefetch_related(
            "fees", "tax_rate", "child_certificates"
        )
        grouped_certificates = group_items_by_parent(certificates)

        return render(
            request,
            self.template_name,
            {
                "form_find_parcel": form_find_parcel,
                "form_create_order_session": form_create_order_session,
                "grouped_certificates": grouped_certificates,
            },
        )

    def post(self, request):
        certificates = Certificate.objects.all()
        grouped_certificates = group_items_by_parent(certificates)
        form_create_order_session = CreateOrderSessionForm(request.POST)

        if form_create_order_session.is_valid():
            data_clean = form_create_order_session.cleaned_data
            result = create_order_session(
                property_id=data_clean["property_id"],
                order_lines=data_clean["lines"],
                customer_name=data_clean["customer_name"],
                customer_company_name=data_clean["customer_company_name"],
            )

            if result and result["success"]:
                dest = result["checkout_url"]
                return redirect(dest)
            elif result and result["error"]:
                form_create_order_session.add_error(None, result["error"])

        # Attempt to pre-fill the form with a valid chosen property.
        property_serialized = None
        form_find_parcel = FindParcelForm()
        if not form_create_order_session.has_error("property_id"):
            property_id = form_create_order_session.cleaned_data["property_id"]
            property_obj = Property.objects.get(id=property_id)
            property_serialized = serialize_property(property_obj)

        return render(
            request,
            self.template_name,
            {
                "form_find_parcel": form_find_parcel,
                "form_create_order_session": form_create_order_session,
                "grouped_certificates": grouped_certificates,
                "submitted": True,
                "property": property_serialized,
            },
        )

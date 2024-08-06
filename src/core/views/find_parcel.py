"""Views for handling property searches and certificate orders."""

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods

from core.forms.find_parcel import FindParcelForm
from core.forms.order.create_order_session import CreateOrderSessionForm
from core.models.certificate import Certificate


@method_decorator(require_http_methods(["GET", "POST"]), name="dispatch")
class FindParcel(View):
    """
    View for handling the find parcel component.

    This view renders the certificate order page and processes
    form submissions for finding parcels.
    """

    template_name = "pages/certificate_order.html"

    def get(self, request):
        """
        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: Rendered certificate order page with an empty form.
        """
        form = FindParcelForm()
        form_create_order_session = CreateOrderSessionForm()
        certificates = Certificate.objects.all()
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "form_create_order_session": form_create_order_session,
                "certificates": certificates,
            },
        )

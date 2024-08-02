"""Views for handling property searches and certificate orders."""

from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from core.forms.find_parcel import FindParcelForm
from core.models.certificate import Certificate
from core.models.fee import Fee


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
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
        certificates = Certificate.objects.all()
        fees = Fee.objects.all()
        return render(request, self.template_name, {"form": form, "certificates": certificates, "fees": fees})

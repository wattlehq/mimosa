"""Views for handling property searches and certificate orders."""
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from core.forms.find_parcel import FindParcelForm
from core.forms.order.create_order_session import CreateOrderSessionForm
from core.models.certificate import Certificate
from core.services.order.create_order_session import create_order_session


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
        form_find_parcel = FindParcelForm()
        form_create_order_session = CreateOrderSessionForm()
        certificates = Certificate.objects.all()
        return render(
            request,
            self.template_name,
            {
                "form_find_parcel": form_find_parcel,
                "form_create_order_session": form_create_order_session,
                "certificates": certificates,
            },
        )

    def post(self, request):
        form_find_parcel = FindParcelForm()
        certificates = Certificate.objects.all()
        form_create_order_session = CreateOrderSessionForm(request.POST)

        if form_create_order_session.is_valid():
            result = create_order_session(
                property_id=form_create_order_session.cleaned_data[
                    "property_id"],
                order_lines=form_create_order_session.cleaned_data["lines"],
                customer_name=form_create_order_session.cleaned_data[
                    "customer_name"],
                customer_company_name=form_create_order_session.cleaned_data[
                    "customer_company_name"]
            )

            if result and result["success"]:
                dest = result["checkout_url"]
                return redirect(dest)
            elif result and result["error"]:
                form_create_order_session.add_error(None, result["error"])
        return render(
            request,
            self.template_name,
            {
                "form_find_parcel": form_find_parcel,
                "form_create_order_session": form_create_order_session,
                "certificates": certificates,
            },
        )

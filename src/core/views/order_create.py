from django.shortcuts import redirect
from django.views import View

from core.forms.order.create_order_session import CreateOrderSessionForm
from core.services.order.create_order_session import create_order_session


class OrderCreate(View):
    def post(self, request):
        form = CreateOrderSessionForm(request.POST)
        if form.is_valid():
            # @todo Handle customer name & business.
            result = create_order_session(
                property_id=form.cleaned_data["property_id"],
                order_lines=form.cleaned_data["lines"],
                customer_name=form.cleaned_data["customer_name"],
                customer_company_name=form.cleaned_data["customer_company_name"]
            )

            if result and result["success"]:
                dest = result["checkout_url"]
                return redirect(dest)
            else:
                # @todo Handle
                pass
        else:
            # @todo Handle form.errors
            pass

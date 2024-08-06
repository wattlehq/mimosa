from django.shortcuts import redirect
from django.views import View

from core.services.order.create_order_session import create_order_session
from forms.order.create_order_session import CreateOrderSessionForm


class OrderCreate(View):
    def post(self, request):
        form = CreateOrderSessionForm(request.POST)
        if form.is_valid():
            # @todo Handle customer name & business.
            result = create_order_session(
                property_id=form.cleaned_data['property_id'],
                order_lines=form.cleaned_data['lines'],
            )

            if result and result['success']:
                dest = result["checkout_url"]
                return redirect(dest)
            else:
                # @todo Handle
                pass
        else:
            # @todo Handle form.errors
            pass

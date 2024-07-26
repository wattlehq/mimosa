from django.shortcuts import render

from core.models.certificate import Certificate
from core.models.fee import Fee

def product_selection(request):
    certificates = Certificate.objects.all()
    fees = Fee.objects.all()
    context = {
        'certificates': certificates,
        'fees': fees
    }
    return render(request, 'pages/product_selection.html', context)


from django.shortcuts import render


def product_selection(request):
    return render(request, 'pages/product_selection.html')

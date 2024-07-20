from django.shortcuts import render

def product_selection_view(request):
    return render(request, 'pages/product_selection.html')
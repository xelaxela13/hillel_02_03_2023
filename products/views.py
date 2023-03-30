from django.shortcuts import render

from products.forms import ProductModelForm
from products.models import Product


def products(request, *args, **kwargs):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
    return render(request, 'products/index.html', context={
        'products': Product.objects.iterator(),
        'form': form
    })

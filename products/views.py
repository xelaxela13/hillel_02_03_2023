import csv

import weasyprint
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView

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


def export_csv(request, *args, **kwargs):
    headers = {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename="products.csv"'
    }
    response = HttpResponse(headers=headers)
    fields_name = ['name', 'description', 'sku', 'image', 'price', 'is_active']
    writer = csv.DictWriter(response, fieldnames=fields_name)
    writer.writeheader()
    for product in Product.objects.iterator():
        writer.writerow(
            {
                'name': product.name,
                'description': product.description,
                'image': product.image.name if product.image else 'no image',
                'sku': product.sku,
                'price': product.price,
                'is_active': product.is_active
            }
        )
    return response


class ExportToPdf(TemplateView):
    template_name = 'products/pdf.html'

    def get(self, request, *args, **kwargs):
        context = {'products': Product.objects.all()}
        headers = {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename="products.pdf"'
        }
        html = render_to_string(
            template_name=self.template_name,
            context=context
        )
        pdf = weasyprint.HTML(string=html).write_pdf()
        response = HttpResponse(pdf, headers=headers)
        return response

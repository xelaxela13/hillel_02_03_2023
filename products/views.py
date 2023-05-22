import csv

import weasyprint
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, ListView, DetailView

from products.forms import ProductModelForm, ImportCSVForm
from products.models import Product, Category
from project.model_choices import ProductCacheKeys


def products(request, *args, **kwargs):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()

    return render(request, 'products/product_list.html', context={
        'products': Product.objects.iterator(),
        'form': form
    })


class ProductDetail(DetailView):
    context_object_name = 'product'
    model = Product

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = cache.get_or_set(f"{ProductCacheKeys.PRODUCTS}_{pk}",
                                   queryset.get())
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query"
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj


class ProductsView(ListView):
    context_object_name = 'products'
    model = Product
    ordering = '-created_at'

    def get_queryset(self):
        queryset = cache.get(ProductCacheKeys.PRODUCTS)
        if not queryset:
            queryset = Product.objects.prefetch_related('categories',
                                                        'products').all()
            cache.set(ProductCacheKeys.PRODUCTS, queryset)

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


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


class ImportCSV(FormView):
    form_class = ImportCSVForm
    template_name = 'products/import_csv.html'
    success_url = reverse_lazy('products')

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProductByCategory(ListView):
    context_object_name = 'products'
    model = Product

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.category = Category.objects.get(slug=kwargs['slug'])
        except Category.DoesNotExist:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        select_related  - FK, OneToOne
        prefetch_related - ManyToMany

        :return:
        """
        qs = super().get_queryset()
        qs = qs.filter(categories__in=(self.category,))
        qs = qs.prefetch_related('products', 'categories', )
        return qs

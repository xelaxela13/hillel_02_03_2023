from django import forms

from products.models import Product
from project.constants import MAX_DIGITS, DECIMAL_PLACES


class ProductForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    sku = forms.CharField()
    price = forms.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    image = forms.ImageField()

    def is_valid(self):
        is_valid = super().is_valid()
        if is_valid:
            try:
                Product.objects.get(name=self.cleaned_data['name'])
                is_valid = False
            except Product.DoesNotExist:
                ...
        return is_valid

    def save(self):
        return Product.objects.create(**self.cleaned_data)


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'sku', 'image', 'price')

    def clean_name(self):
        try:
            Product.objects.get(name=self.cleaned_data['name'])
            raise ValidationError('Product already exist.')
        except Product.DoesNotExist:
            ...
        return self.cleaned_data['name']


import csv
import decimal
from io import StringIO

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from products.models import Product, Category


class ImportCSVForm(forms.Form):
    file = forms.FileField(
        validators=[FileExtensionValidator(['csv'])]
    )

    def clean_file(self):
        csv_file = self.cleaned_data['file']
        reader = csv.DictReader(StringIO(csv_file.read().decode('utf-8')))
        products_list = []
        for product in reader:
            try:
                products_list.append(
                    Product(
                        name=product['name'],
                        description=product['description'],
                        price=decimal.Decimal(product['price']),
                        sku=product['sku'],
                        is_active=product['is_active']
                    )
                )
            except (KeyError, decimal.InvalidOperation) as err:
                raise ValidationError(err)
        if not products_list:
            raise ValidationError('Wrong file format.')
        return products_list

    def save(self):
        products_list = self.cleaned_data['file']
        Product.objects.bulk_create(products_list)

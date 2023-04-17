from django.urls import path

from products.views import products, export_csv, ExportToPdf

urlpatterns = [
    path('', products, name='products'),
    path('export-csv/', export_csv, name='products_to_csv'),
    path('export-pdf/', ExportToPdf.as_view(), name='products_to_pdf'),
]

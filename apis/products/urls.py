from django.urls import path

from apis.products.views import ProductList

urlpatterns = [
    path('products/', ProductList.as_view()),
]

"""
GET /api/v1/products/
POST /api/v1/products/
PUT /api/v1/products/ID
DELETE /api/v1/products/ID
"""

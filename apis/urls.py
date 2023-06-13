from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apis.orders.urls import urlpatterns as api_orders_urlpatterns
from apis.products.urls import urlpatterns as api_products_urlpatterns

api_urlpatterns = [
    *api_products_urlpatterns,
    *api_orders_urlpatterns
]
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='jwt_login'),
    path('refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    *api_urlpatterns
]

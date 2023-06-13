from rest_framework.routers import SimpleRouter

from apis.products.views import ProductViewSet

router = SimpleRouter()
router.register(r'products', ProductViewSet, basename='products')
urlpatterns = router.urls
#
# urlpatterns = [
#     path('products/', ProductList.as_view()),
#     path('products/create/', ProductCreate.as_view()),
#     path('products/<uuid:pk>/detail/', ProductDetail.as_view()),
#     path('products/<uuid:pk>/delete/', ProductDelete.as_view()),
# ]

"""
GET /api/v1/products/
POST /api/v1/products/
PUT /api/v1/products/ID
DELETE /api/v1/products/ID
"""

from rest_framework.routers import SimpleRouter

from apis.orders.views import OrderViewSet

router = SimpleRouter()
router.register(r'orders', OrderViewSet, basename='orders')
urlpatterns = router.urls

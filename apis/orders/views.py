from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apis.orders.serializers import OrderSerializer
from orders.models import Order


class OrderViewSet(mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    @action(methods=('GET',), detail=False, url_path='current',
            serializer_class=OrderSerializer)
    def current(self, request):
        qs = self.get_queryset()
        order = qs.filter(is_active=True, is_paid=False).first()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

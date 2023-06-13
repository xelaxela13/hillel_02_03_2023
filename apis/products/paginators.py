from rest_framework.pagination import PageNumberPagination


class ProductPaginator(PageNumberPagination):
    page_size = 4
    ordering = 'created_at'

from django.urls import reverse

from products.models import Product
from project.constants import MAX_DIGITS, DECIMAL_PLACES


def test_products_list(client, faker):
    for _ in range(3):
        Product.objects.create(
            name=faker.word(),
            sku=faker.word(),
            price=faker.pydecimal(
                min_value=0,
                left_digits=DECIMAL_PLACES,
                right_digits=MAX_DIGITS - DECIMAL_PLACES,
            )
        )
    url = reverse('products')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['products']) == Product.objects.count()

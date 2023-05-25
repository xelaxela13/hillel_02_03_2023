import os

import factory
import faker
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_factoryboy import register

from currencies.models import CurrencyHistory
from products.models import Product, Category
from project.constants import DECIMAL_PLACES

fake = faker.Faker()


@pytest.fixture(scope='session')
def faker_fixture():
    yield fake


@pytest.fixture(autouse=True)
def django_db_setup(db):
    import shutil
    from django.conf import settings
    media_root = settings.BASE_DIR / settings.MEDIA_ROOT
    if not os.path.exists(media_root):
        os.mkdir(media_root)
    yield
    shutil.rmtree(media_root)


@register
class UserFactory(factory.django.DjangoModelFactory):
    email = factory.LazyAttribute(lambda x: fake.email())
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    last_name = factory.LazyAttribute(lambda x: fake.last_name())
    phone = factory.LazyAttribute(lambda x: fake.phone_number())
    is_phone_valid = True

    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)


@register
class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda x: fake.word())

    class Meta:
        model = Category
        django_get_or_create = ('name',)


@register
class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda x: fake.word())
    sku = factory.LazyAttribute(lambda x: fake.word())
    description = factory.LazyAttribute(lambda x: fake.sentence())
    image = factory.django.ImageField()
    price = factory.LazyAttribute(lambda x: fake.pydecimal(
        min_value=0,
        left_digits=DECIMAL_PLACES,
        right_digits=DECIMAL_PLACES,
    ))

    class Meta:
        model = Product
        django_get_or_create = ('name', 'sku')

    @factory.post_generation
    def post(self, create, extracted, **kwargs):
        self.categories.add(CategoryFactory())


@pytest.fixture(scope='function')
def login_client(db, client):
    def login_user(user=None, **kwargs):
        if user is None:
            user = UserFactory()
        user.set_password('123456789')
        user.save()
        response = client.post(reverse('login'),
                               data={'username': user.email,
                                     'password': '123456789'}
                               )
        assert response.status_code == 302
        return client, user

    return login_user


@register
class CurrencyHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CurrencyHistory

    code = factory.LazyAttribute(lambda x: fake.word())
    buy = factory.LazyAttribute(lambda x: fake.pydecimal(
        min_value=0,
        left_digits=DECIMAL_PLACES,
        right_digits=DECIMAL_PLACES,
    ))
    sale = factory.LazyAttribute(lambda x: fake.pydecimal(
        min_value=0,
        left_digits=DECIMAL_PLACES,
        right_digits=DECIMAL_PLACES,
    ))

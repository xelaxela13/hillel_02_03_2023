import faker
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, IntegrityError, DataError

from products.models import Product, Category

fake = faker.Faker()
class Command(BaseCommand):
    help = "Create fake products"


    def add_arguments(self, parser):
        parser.add_argument("-c", "--count", type=int, default=5)

    def handle(self, *args, **options):
        real_count = 0
        category_name = fake.word()

        def do_something():
            self.stdout.write(
                self.style.SUCCESS("do_something")
            )

        for i in range(options.get('count')):
            try:
                with transaction.atomic():
                    transaction.on_commit(do_something)
                    product = Product.objects.create(
                        name=fake.sentence(nb_words=30, variable_nb_words=True),
                        description=fake.sentence(),
                        sku=fake.random_number(),
                        price=fake.pydecimal(left_digits=4, right_digits=2,
                                             positive=True)
                    )
                    product.categories.add(
                        Category.objects.create(
                            name=fake.word(),
                            description=fake.sentence(),
                        )
                    )
                    real_count += 1
            except (IntegrityError, DataError) as err:
                self.stdout.write(
                    self.style.ERROR(err)
                )
        self.stdout.write(
            self.style.SUCCESS('Successfully closed poll "%s"' % real_count)
        )

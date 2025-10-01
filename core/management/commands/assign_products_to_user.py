from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import ProductInstance


class Command(BaseCommand):
    help = "Assigns all existing products without a user to a specified user"

    def add_arguments(self, parser):
        parser.add_argument(
            "username", type=str, help="Username of the user to assign products to"
        )

    def handle(self, *args, **options):
        username = options["username"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist'))
            return

        # Get all products that don't have a user assigned
        products = ProductInstance.objects.filter(user__isnull=True)
        count = products.count()

        if count == 0:
            self.stdout.write(self.style.WARNING("No products found without a user"))
            return

        # Assign the user to all these products
        products.update(user=user)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully assigned {count} products to user "{username}"'
            )
        )

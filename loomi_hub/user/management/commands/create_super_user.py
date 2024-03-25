from django.db import transaction
from django.core.management import BaseCommand

from loomi_hub.user.models import User


class Command(BaseCommand):
    help = "Create roles, admin user, and general app's users"

    @transaction.atomic
    def handle(self, *args, **options):
        self.create_users()

    def create_users(self):
        # Creates Admin user to log in on Django Admin (http://localhost:8000/admin)
        User.objects.create_superuser(username='admin', email='admin@super.com', password='@Abc123456',
                                      first_name='admin',
                                      last_name='admin')
        self.stdout.write(self.style.SUCCESS('Admin user created successfully'))

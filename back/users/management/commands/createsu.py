from django.core.management.base import BaseCommand
from users.models import Student


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Student.objects.filter(username="admin").exists():
            Student.objects.create_superuser("admin", "dhruvkabaiya1@gmail.com", "admin")
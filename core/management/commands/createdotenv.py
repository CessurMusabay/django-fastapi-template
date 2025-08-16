from django.core.management.base import BaseCommand
from config import Settings


class Command(BaseCommand):
    help = "Create .env file"

    def handle(self, *args, **options):
        Settings.generate_env_file()

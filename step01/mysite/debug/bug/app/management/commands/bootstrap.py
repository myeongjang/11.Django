from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):

    def handle(self, *args, **options):
        with transaction.atomic():
            call_command('migrate')

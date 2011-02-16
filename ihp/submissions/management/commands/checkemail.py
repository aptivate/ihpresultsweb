import sys
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core import management
from submissions.pop import poll

class Command(BaseCommand):
    args = "[No args needs]"
    help = "Poll email account for new submissions"

    def handle(self, *args, **options):
        if len(args) == 0:
            poll()
        else:
            raise CommandError("Expected 0")

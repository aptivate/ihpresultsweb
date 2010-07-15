import sys
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core import management
from submissions.helpers import load_agency_targets

class Command(BaseCommand):
    args = "[file to parse]"
    help = "Loads targets from a file or url"

    def handle(self, *args, **options):
        if len(args) == 1:
            filename = args[0]
            load_agency_targets(filename)
        elif len(args) == 0:
            load_agency_targets()
        else:
            raise CommandError("Expected 0 or 1 parameters")

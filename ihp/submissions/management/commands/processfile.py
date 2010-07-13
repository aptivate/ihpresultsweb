import sys
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core import management
from submissions.helpers import parse_file

class Command(BaseCommand):
    args = "[file to parse]"
    help = "Parses a questionnaire file - the file may be given as a command line argument. Alternatively, an email address (configured in settings.py) will be checked and any attachements processed"

    def handle(self, *args, **options):
        if len(args) == 1:
            filename = args[0]
            parse_file(filename)
        elif len(args) == 0:
            print "Downloading email - UNDER CONSTRUCTION"
        else:
            raise CommandError("Expected 0 or 1 parameters")

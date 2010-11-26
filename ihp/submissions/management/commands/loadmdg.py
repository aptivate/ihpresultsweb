import sys
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core import management
from submissions.helpers import parse_mdg_file

class Command(BaseCommand):
    args = "[mdg file to parse]"
    help = "Parses an mdg input file"

    def handle(self, *args, **options):
        if len(args) == 1:
            filename = args[0]
            parse_mdg_file(filename)
        else:
            raise CommandError("Expected 1 parameters")

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.core import management
import os


class Command(BaseCommand):
    args = '<No arguments>'
    help = 'This command will reset the database and load all fixtures.'

    def handle(self, *args, **options):
        raise CommandError('Command absolute, please use "./manage dba_init_db" ')

            

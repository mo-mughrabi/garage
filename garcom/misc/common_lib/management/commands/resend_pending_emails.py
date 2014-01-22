from django.core.management.base import BaseCommand
from garcom.misc.common_lib import tasks


class Command(BaseCommand):
    args = '<No arguments>'
    help = 'This command interface will fire up the fire_pending_emails() task through celery.'

    def handle(self, *args, **options):
        tasks.fire_pending_email.delay()
        print 'task fire_pending_emails is sent to celery'

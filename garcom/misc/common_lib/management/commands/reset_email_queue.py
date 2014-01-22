from django.core.management.base import BaseCommand, CommandError
from ...models import NotificationEmail, Notification

class Command(BaseCommand):
    args = '<No arguments>'
    help = 'This command interface will reset all the queued emails.'

    def handle(self, *args, **options):
        row_count = Notification.objects.filter(status=Notification.STATUS_PENDING).update(status=Notification.STATUS_FAILED)
        print 'operation completed with %s updated' % str(row_count)

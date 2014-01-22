from django.conf import settings
from django.db import models
from django.db.models.loading import get_model
from django.utils.translation import get_language
import tasks


class NotificationManager(models.Manager):
    def send_email(self, send_to, subject, text_body, html_body=None, language=None, template=None):
        notification = self.create()
        notification.save()

        get_model('common_lib', 'NotificationEmail').objects.create(
            send_to=send_to,
            subject=subject,
            text_body=text_body,
            html_body=html_body,
            notification=notification,
            language=language if language is not None else get_language()
        ).save()

        tasks.fire_pending_email.delay()

        return notification


class Notification(models.Model):
    """ Notification will be used entirely to contain all outgoing communication Emails/SMS """
    _notification_types = (
        (u'E', 'Emails'),
        (u'S', 'SMS'),
    )
    _notification_type_default = u'E'

    STATUS_PENDING = u'P'
    STATUS_SENT = u'S'
    STATUS_FAILED = u'F'

    _statuses = (
        (u'P', 'Pending'),
        (u'S', 'Sent'),
        (u'F', 'Failed'),
    )
    _status_default = u'P'

    type = models.CharField(
        max_length=1,
        choices=_notification_types,
        default=_notification_type_default
    )
    status = models.CharField(
        max_length=1,
        choices=_statuses,
        default=_status_default,
        db_index=True,
    )

    objects = NotificationManager()


class NotificationEmail(models.Model):
    """
    """

    _default_template = '' # to be decided later

    notification = models.OneToOneField(Notification)
    send_to = models.EmailField()
    # set get_language() as the field default value otherwise
    # if value cannot be retrieved, set default value using LANGUAGE_CODE from setting.py
    language = models.CharField(max_length=10,
                                default=get_language() if get_language() else getattr(settings, 'LANGUAGE_CODE'))
    template = models.CharField(
        max_length=100,
        default=_default_template
    )

    subject = models.CharField(
        max_length=100,
    )

    html_body = models.TextField(
        null=True,
        blank=True
    )
    text_body = models.TextField(

    )


    class Meta:
        db_table = 'common_lib_notification_email'


class NotificationSMS(models.Model):
    notification = models.OneToOneField(Notification)
    destination = models.CharField(
        max_length=100,
    )
    message = models.CharField(
        max_length=400,
    )

    class Meta:
        db_table = 'common_lib_notification_sms'
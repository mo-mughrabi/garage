# -*- coding: utf-8 -*-
from celery.task import task
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.db import transaction
from django.db.models.loading import get_model
import logging
from django.utils.translation import activate

logging.getLogger(__name__)


@task(name='common_lib.send_notification', ignore_result=True)
@transaction.commit_manually
def fire_pending_email():
    Notification = get_model('common_lib', 'Notification')
    NotificationEmail = get_model('common_lib', 'NotificationEmail')

    for email in NotificationEmail.objects.filter(notification__status=Notification.STATUS_PENDING):
        try:
            # set default language
            # this will invoke translations if set to
            # foreign language
            activate(email.language)

            msg = EmailMultiAlternatives(email.subject, email.text_body, getattr(settings, 'OUTGOING_EMAILS'),
                                         [email.send_to, ])
            if email.html_body:
                msg.attach_alternative(email.html_body, "text/html")
            msg.send()
            Notification.objects.filter(pk=email.notification_id).update(status=Notification.STATUS_SENT)
        except Exception as e:
            logging.error(str(e))
            Notification.objects.filter(pk=email.notification_id).update(status=Notification.STATUS_FAILED)
        finally:
            transaction.commit()

    return 'Completed'


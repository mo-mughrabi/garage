# -*- coding: utf-8 -*-
from binascii import hexlify
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.conf import settings
from django.template.context import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
import datetime
import random
import string
import logging
import os
from django.utils import timezone
from social_auth.signals import socialauth_registered, pre_update

# initiate logger
from garcom.misc.common_lib.models import Notification

logging.getLogger(__name__)


# unique attribute would also apply db_index
User._meta.get_field("email")._unique = True
User._meta.get_field("email").db_index = True


class Commercial(models.Model):
    name = models.CharField(max_length=100, )
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(
        blank=True, null=True, upload_to='commercial_profiles/')
    address = models.CharField(max_length=200, null=True, blank=True)

    created_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_create")
    created_at = models.DateTimeField(auto_created=True)
    updated_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_update")
    updated_at = models.DateTimeField(auto_now_add=True)


class CommercialOffice(models.Model):
    commercial = models.ForeignKey(Commercial, )
    main_office = models.BooleanField(default=True)
    address = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    fax = models.CharField(
        max_length=20, null=True, blank=True)

    created_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_create")
    created_at = models.DateTimeField(auto_created=True)
    updated_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_update")
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accounts_commercial_office'


class CommercialProfile(models.Model):
    commercial = models.ForeignKey(Commercial)
    profile = models.ForeignKey('Profile')

    class Meta:
        db_table = 'accounts_commercial_profile'
        unique_together = (
            'commercial', 'profile'
        )


class Profile(models.Model):
    STATUS_INDIVIDUAL = u'I'
    STATUS_CORPORATE = u'C'

    _profile_types = (
        (STATUS_INDIVIDUAL, 'Individual'),
        (STATUS_CORPORATE, 'Corporate'),
    )
    _default_profile_class = u'I'

    user = models.OneToOneField(User)

    # columns used for account activation
    activation_code = models.CharField(max_length=100)
    activation_usage = models.CharField(max_length=2, default=0)
    activation_expiry = models.DateTimeField(null=True, blank=True)

    type = models.CharField(
        choices=_profile_types, max_length=1, default=_default_profile_class)

    preferred_language = models.CharField(
        max_length=5, default=getattr(settings, 'LANGUAGE_CODE', 'en'))

    primary_phone = models.OneToOneField(
        'Phone', related_name='is_primary', null=True, blank=True)
    primary_payment = models.OneToOneField(
        'Payment', related_name='is_primary', null=True, blank=True)


    def __unicode__(self):
        return u'%s' % self.user.username

    @models.permalink
    def get_activation_url(self):
        return ('accounts-verify', (), {
            'verification_code': self.activation_code
        }
        )

    def save(self, force_insert=False, force_update=False, using=None):

        if self.activation_code in ('', u'', None):
            while True:
                code = hexlify(os.urandom(5))
                self.activation_code = code
                if not Profile.objects.filter(activation_code=code).exists():
                    break

        super(Profile, self).save(force_insert=False,
                                  force_update=False, using=None)


class Phone(models.Model):
    _phone_types = (
        (u'MOBI', 'Mobile'),
        (u'HOME', 'Home'),
        (u'FAX', 'Fax'),
    )

    profile = models.ForeignKey(Profile, editable=False)
    type = models.CharField(choices=_phone_types, max_length=16, null=False, blank=False)
    number = models.CharField(max_length=32, null=False, blank=False)

    def __unicode__(self):
        return u'%s' % self.number


class Payment(models.Model):
    _payment_types = (
        ('Debit Card', (
            (u'NBK', 'NBK'),
            (u'GBK', 'GulfBank'),
        )
        ),
        ('Credit Card', (
            (u'VISA', 'Visa'),
            (u'MC', 'MasterCard'),
            (u'AMX', 'American Express'),
        )
        ),
    )

    profile = models.ForeignKey(Profile, editable=False)
    type = models.CharField(
        choices=_payment_types, max_length=16, null=False, blank=False)
    number = models.CharField(
        max_length=32, null=False, blank=False)


class PasswordRecoveryManager(models.Manager):
    def set_random_password(self, password_recovery):
        try:
            random_password = ''.join(
                random.choice(string.letters) for i in xrange(getattr(settings, 'SF_PASS_PHRASE_LENGTH', 15)))
            user = User.objects.get(pk=password_recovery.user.id)
            user.set_password(random_password)
            user.save()
            return random_password
        except:
            return False

    def is_valid(self, pass_phrase):
        try:
            obj = self.get_query_set().get(pass_phrase=pass_phrase, pass_usage='N',
                                           expires_at__gte=datetime.datetime.now())
            obj.pass_usage = 'U'
            obj.save()
            return obj
        except self.model.DoesNotExist:
            return False

    def create_pass_phrase(self, email, requestor_ip):

        random_pass_phrase = ''.join(
            random.choice(string.letters) for i in xrange(getattr(settings, 'GARAGE_PASS_PHRASE_LENGTH', 15)))

        try:
            # first make sure random string is unique to the user
            # if exists then recursively call the same function
            # until a random pass phrase is found

            self.get(pass_phrase=random_pass_phrase,
                     user=User.objects.get(email=email))
            self.create_pass_phrase(email, requestor_ip)

        except self.model.DoesNotExist:

            rec = self.create(
                user=User.objects.get(email=email),
                requestor_ip=requestor_ip,
                expires_at=datetime.datetime.now() + datetime.timedelta(
                    hours=getattr(settings, 'SF_PASS_PHRASE_EXPIRY', 2)),
                pass_phrase=random_pass_phrase,
            )
            rec.save()
            return rec
        except Exception as e:
            raise e


class PasswordRecovery(models.Model):
    STATUS_USED = 'U'
    STATUS_NEW = 'N'
    _pass_usages = (
        (STATUS_USED, _('Used')),
        (STATUS_NEW, _('New'))
    )
    _pass_usages_default = 'N'

    user = models.ForeignKey(User, db_index=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)
    requestor_ip = models.IPAddressField()

    pass_phrase = models.CharField(max_length=100)
    pass_usage = models.CharField(
        max_length=2, choices=_pass_usages, default=_pass_usages_default)

    objects = PasswordRecoveryManager()

    class Meta:
        db_table = 'accounts_password_recovery'


class Watched(models.Model):
    pass


class MyUserManager(UserManager):
    def create_user(self, username, email=None, password=None):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)

        try:
            user = self.get(email=email)
        except self.model.DoesNotExist:
            user = self.model(username=username, email=email,
                              is_staff=False, is_active=True, is_superuser=False,
                              last_login=now, date_joined=now)

            user.set_password(password)
            user.save(using=self._db)

        return user


manager = MyUserManager()
manager.contribute_to_class(User, 'objects')


def create_user_profile(sender, instance, created, **kwargs):
    """ create_user_profile signal would create a new recover in profile
    table when a new user is created with its default values. """
    if created:
        user_profile = Profile.objects.create(user=instance)


def social_auth_new_users_handler(sender, user, response, details, **kwargs):
    """
    social_auth_new_users_handler: is a signal that fires when a new user signs up using
    social authentication. Currently it would do the following

        1. send out an email for the user congratulating him for signing up

    """
    html = get_template('accounts/email_template/social_auth_new_users.html')
    txt = get_template('accounts/email_template/social_auth_new_users.txt')
    c = Context({
        'user': user.first_name,
    })
    Notification.objects.send_email(
        send_to=user.email,
        subject=_('Welcome to Garage'),
        html_body=html.render(c),
        text_body=txt.render(c)
    )

    return False


socialauth_registered.connect(social_auth_new_users_handler, sender=None,
                              dispatch_uid="accounts.social_auth_new_users_handler")
post_save.connect(create_user_profile, sender=User,
                  dispatch_uid="accounts.create.user.profile")

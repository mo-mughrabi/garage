# -*- coding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Max
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import get_template
from forms import UserForm, PaymentInlineForm, LoginForm, PhoneInlineForm, RecoveryForm, RegistrationForm
from garcom.misc.common_lib.models import Notification
from models import Profile, Payment, Phone, PasswordRecovery
from django.conf import settings
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import redirect, render_to_response
from django.utils.translation import ugettext_lazy as _
from ...misc.common_lib.decorators import anonymous_required
import logging
from django.template import Context


# initiate logger
logging.getLogger(__name__)


def login(request, async=False):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid:
            data = form.data
            user = authenticate(
                username=data.get('email'), password=data.get('password'))
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return redirect(reverse('vehicle-index') if not request.POST.get('next', None) else request.POST.get('next', None))
                else:
                    # message when user is not active
                    messages.error(request, _('Your account is not activated, please click on the activation link sent via email.'))
            else:
                # message when email or password are invalid
                messages.error(request, _(
                    'Invalid email or password, please try again.'))
        else:
            # message when form is invalid (left blank fields)
            messages.error(
                request, _('Invalid email or password, please try again.'))
    else:
        form = LoginForm(initial={'next': request.GET.get('next', None)})

    return render_to_response(
        'accounts/login.html',
        {
            'form': form,
        },
        RequestContext(request)

    )


def logout(request):
    django_logout(request)
    return redirect(reverse('vehicle-index'))


def index(request):
    return redirect(reverse('accounts-profile'))


@anonymous_required
def register(request):
    """
    registration

    """

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            object = form.save(commit=False)
            object.username = 'GAR%i' % (int(
                form.Meta.model.objects.aggregate(Max('id'))['id__max']) + 1)
            object.is_active = False
            object.set_password(data.get('password'))
            object.save()
            object.profile.preferred_language = request.LANGUAGE_CODE

            messages.success(request, _(
                'Congratulations, you are now member of Garage network.'))

            html = get_template('accounts/email_template/new_register.html')
            txt = get_template('accounts/email_template/new_register.txt')

            c = Context({
                'user': object.first_name,
                'activation_link': object.profile.get_activation_url(),
                'domain': request.META['HTTP_HOST'],
                'protocol': 'https' if request.is_secure() else 'http'
            })

            Notification.objects.send_email(
                send_to=object.email,
                subject=_('Welcome to Garage'),
                html_body=html.render(c),
                text_body=txt.render(c)
            )
            return redirect(reverse('accounts-login'))

    else:
        form = RegistrationForm()

    return render_to_response(
        'accounts/register.html',
        {
            'form': form,
        },
        RequestContext(request)
    )


@anonymous_required
def verify_account(request, verification_code):
    """
    verify_account:

    """
    try:
        user_profile = Profile.objects.get(activation_code=verification_code)
        user_profile.user.is_active = True
        user_profile.user.save()
        return redirect(reverse('accounts-profile-my-vehicles'))

    except Profile.DoesNotExist as e:
        raise Http404


@anonymous_required
def recovery(request, pass_phrase=None):
    """
    recovery: is used to recover the account credentials if forgotten
    """
    if pass_phrase:
        pass_recovery = PasswordRecovery.objects.is_valid(pass_phrase=pass_phrase)
        if pass_recovery:
            random_password = PasswordRecovery.objects.set_random_password(pass_recovery)

            c = Context({
                'user': pass_recovery.user.username,
                'password': random_password,
                'domain': request.META['HTTP_HOST'],
                'protocol': 'https' if request.is_secure() else 'http'
            })

            html = get_template('accounts/email_template/password_recovery_reset-pass.html')
            txt = get_template('accounts/email_template/password_recovery_reset-pass.txt')

            msg = EmailMultiAlternatives('Password reset Garage', txt.render(c), getattr(settings, 'OUTGOING_EMAILS'),
                                         [pass_recovery.user.email, ])
            msg.attach_alternative(html.render(c), "text/html")
            msg.send()

            messages.success(request, _(
                'A new password is generated and sent to your email box.'))
            return redirect(reverse('accounts-login'))


    if request.method == 'POST':
        form = RecoveryForm(request.POST)
        if form.is_valid():
            messages.success(
                request, _('An email is sent to you for verification.'))
            pass_recovery = PasswordRecovery.objects.create_pass_phrase(
                form.cleaned_data['email'], request.META.get('REMOTE_ADDR'))

            c = Context({
                'user': pass_recovery.user.username,
                'password_recovery_link': reverse('accounts-recovery-pass-phrase', args=[pass_recovery.pass_phrase, ]),
                'password_expiry': getattr(settings, 'SF_PASS_PHRASE_EXPIRY', 4),
                'domain': request.META['HTTP_HOST'],
                'protocol': 'https' if request.is_secure() else 'http'
            })

            html = get_template('accounts/email_template/password_recovery_request-link.html')
            txt = get_template('accounts/email_template/password_recovery_request-link.txt')

            msg = EmailMultiAlternatives('Password reset Garage', txt.render(c), getattr(settings, 'OUTGOING_EMAILS'),
                                         [pass_recovery.user.email, ])
            msg.attach_alternative(html.render(c), "text/html")
            msg.send()

            return redirect(reverse('accounts-login'))
    else:
        form = RecoveryForm()

    return render_to_response(
        'accounts/recovery.html',
        {
            'form': form
        },
        RequestContext(request)
    )


@login_required
def profile(request):

    return render_to_response(
        'accounts/profile/main.html',
        {
            'user': request.user,
            'profile': request.user.get_profile,
        },
        RequestContext(request)
    )


@login_required
def profile_general(request):

    if request.method == 'POST':
        UserInfoForm = UserForm(request.POST, instance=request.user)

        if UserInfoForm.is_valid():
            try:
                # save forms
                UserInfoForm.save()
                messages.success(request, _(
                    'Your information have been updated successfully.'))
            except ValueError as e:
                messages.error(request, _('Invalid information, please correct the fields in Red below.'))
    else:
        UserInfoForm = UserForm(instance=request.user)

    return render_to_response(
        'accounts/profile/general.html',
        {
            'email': request.user.email,
            'UserForm': UserInfoForm,
        },
        RequestContext(request)
    )


@login_required
def profile_payments(request, make_primary=None, delete_payment=None):

    # retrieve user profile
    user_profile = request.user.get_profile()

    # if make_primary is specified, make the payment primary
    if make_primary:
        try:
            user_profile.primary_payment = Payment.objects.filter(
                profile=request.user.get_profile()).get(pk=make_primary)
            user_profile.save()
        except Payment.DoesNotExist:
            pass

    # if delete_payment is specified, delete the payment
    if delete_payment:
        try:
            payment = Payment.objects.filter(
                profile=user_profile).get(pk=delete_payment)
            if user_profile.primary_payment != payment:
                payment.delete()
                messages.success(request, _('Payment has been deleted.'))
            else:
                messages.error(
                    request, _('Primary payment cannot be deleted.'))
        except Payment.DoesNotExist:
            messages.error(request, _('Payment could not be deleted.'))
            pass

    PaymentsFormSet = inlineformset_factory(
        Profile,
        Payment,
        extra=settings.GARAGE_INDIV_INITIAL_PAYMENTS,
        max_num=settings.GARAGE_INDIV_MAX_PAYMENTS,
        form=PaymentInlineForm
    )

    if request.method == 'POST':
        PaymentsForm = PaymentsFormSet(request.POST, instance=user_profile)

        if PaymentsForm.is_valid():
            messages.success(
                request, _('Your payments have been updated successfully.'))

            PaymentsForm.save()
            PaymentsForm = PaymentsFormSet(instance=user_profile)
        else:
            messages.error(request, _('Invalid information, please correct the highlighted cards in red below.'))
    else:
        PaymentsForm = PaymentsFormSet(instance=user_profile)

    return render_to_response(
        'accounts/profile/payments.html',
        {
            'PaymentsForm': PaymentsForm,
            'profile': user_profile,
        },
        RequestContext(request)
    )


@login_required
def profile_contacts(request, make_primary=None, delete_phone=None):

    # retrieve user profile
    user_profile = request.user.get_profile()

    # if make_primary is specified, make the phone primary
    if make_primary:
        try:
            user_profile.primary_phone = Phone.objects.filter(
                profile=user_profile).get(pk=make_primary)
            user_profile.save()
        except Phone.DoesNotExist:
            pass

    # if delete_phone is specified, delete the phone
    if delete_phone:
        try:
            # TODO: Must create validation here to make sure user cannot delete
            # all his numbers in case he is using "Show phone numbers" in
            # privacy settings

            phone = Phone.objects.filter(
                profile=user_profile).get(pk=delete_phone)
            if user_profile.primary_phone != phone:
                phone.delete()
                messages.success(request, _('Phone has been deleted.'))
            else:
                messages.error(request, _('Primary phone cannot be deleted.'))
        except Phone.DoesNotExist:
            messages.error(request, _('Phone could not be deleted.'))
            pass

    PhonesFormSet = inlineformset_factory(
        Profile,
        Phone,
        extra=getattr(settings, 'GARAGE_INDIV_INITIAL_PHONES', None),
        max_num=getattr(settings, 'GARAGE_INDIV_MAX_PHONES', None),
        form=PhoneInlineForm
    )

    if request.method == 'POST':
        PhonesForm = PhonesFormSet(request.POST, instance=user_profile)

        if PhonesForm.is_valid():
            messages.success(
                request, _('Your contacts have been updated successfully.'))

            PhonesForm.save()
            PhonesForm = PhonesFormSet(instance=user_profile)

    else:
        PhonesForm = PhonesFormSet(instance=user_profile)

    return render_to_response(
        'accounts/profile/contacts.html',
        {
            'formset': PhonesForm,
            'profile': user_profile,
        },
        RequestContext(request)
    )



@login_required
def my_vehicle(request):
    return render_to_response(
        'accounts/profile/my_vehicle.html',
        {},
        RequestContext(request)
    )

# -*- coding: utf-8 -*-
import logging
import datetime

from django.core.urlresolvers import reverse
from django.db.models import F
from django.http import Http404, HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404
from django.template.context import Context
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.utils.timezone import utc

from garcom.misc.common_lib.models import Notification
from models import Car, Image
from forms import CarForm, ModelLookUpForm, ModelLookUpI18nForm
import tasks
from celery.execute import send_task


logging.getLogger(__name__)


def index(request):
    return render_to_response(
        'index.html', {},
        RequestContext(request)
    )


def profile(request, year, make, model, hex_id):
    """

    """
    car = get_object_or_404(Car, id=int(hex_id, 16))
    images = Image.objects.filter(car=car)

    if car.status not in (Car.STATUS_ACTIVE, Car.STATUS_SOLD) and not request.user.is_staff:
        # only staff can view non-active posts
        raise Http404


    # only allow owner to view a Pending or Draft post
    if car.status in (Car.STATUS_PENDING, Car.STATUS_DRAFT) and request.user != car.created_by:
        return HttpResponseForbidden()

    try:
        tasks.add_view_count.delay(car.id)
    except Exception as e:
        Car.objects.filter(
            pk=id).update(view_count=F('view_count') + 1)


    return render_to_response(
        'vehicle/profile.html',
        {
            'car': car,
            'images': images,
        },
        context_instance=RequestContext(request)
    )




@login_required
def approve(request):
    try:
        # user must have is_staff right
        if not request.user.is_staff: return Http404
        if request.method == 'POST':
            for i in request.POST.getlist('cars', None):
                object = Car.objects.get(pk=i)
                if request.POST.get('action', None) == 'A':
                    object.approved_by = request.user
                    object.approved_at = datetime.datetime.utcnow().replace(tzinfo=utc)
                    object.status = object.STATUS_ACTIVE

                    email_html = get_template('vehicle/email_template/vehicle_approved.html')
                    email_txt = get_template('vehicle/email_template/vehicle_approved.txt')
                    email_subject = _('Your car in Garage has been approved')

                else:
                    object.status = object.STATUS_REJECTED

                    email_html = get_template('vehicle/email_template/vehicle_rejected.html')
                    email_txt = get_template('vehicle/email_template/vehicle_rejected.txt')
                    email_subject = _('Your car in Garage has been rejected')

                c = Context({
                    'user': object.created_by.first_name,
                    'model': object.get_model_display(),
                    'get_absolute_url': object.get_absolute_url(),
                    'domain': request.META['HTTP_HOST'],
                    'protocol': 'https' if request.is_secure() else 'http'
                })

                Notification.objects.send_email(
                    send_to=object.created_by.email,
                    subject=email_subject,
                    html_body=email_html.render(c),
                    text_body=email_txt.render(c),
                    language=object.created_by.get_profile().preferred_language
                )

                messages.success(request, _('Vehicle updated successfully.'))
                object.save()

                return redirect(reverse('vehicle-approve'))

        return render_to_response(
            'vehicle/approve.html',
            {
                'cars': Car.objects.filter(status=Car.STATUS_PENDING)
            },
            context_instance=RequestContext(request)
        )


    except Exception as e:
        logging.error(str(e))
        raise Http404

    finally:
        pass


@login_required()
def edit(request, id):
    pass


@login_required
def new(request):
    form = None
    try:

        if request.method == 'POST':
            if request.POST.get('id'):
                #edit operations
                pass

            form = CarForm(request.POST, user=request.user)

            if form.is_valid():
                obj = form.save(commit=False)
                obj.created_by = request.user
                obj.save()

            # save record and redirect
            return redirect('/')
        else:
            # edit mode for draft
            form = CarForm(instance=Car.objects.get(status=Car.STATUS_DRAFT, created_by=request.user), user=request.user)
            model_lookup_form = ModelLookUpForm()
            model_lookup_i18n_form = ModelLookUpI18nForm()

        return render_to_response(
            'vehicle/new.html',
            {
                'model_lookup_form': model_lookup_form,
                'model_lookup_i18n_form': model_lookup_i18n_form,
                'form': form,
            },
            RequestContext(request)
        )


    except (Car.DoesNotExist, Car.MultipleObjectsReturned) as e:
        # new form (no drafts found)

        model_lookup_form = ModelLookUpForm()
        model_lookup_i18n_form = ModelLookUpI18nForm()
        form = CarForm(user=request.user)

        return render_to_response(
            'vehicle/new.html',
            {
                'model_lookup_form': model_lookup_form,
                'model_lookup_i18n_form': model_lookup_i18n_form,
                'form': form,
            },
            RequestContext(request)
        )

    except Exception as e:
        logging.error(str(e))
        raise Http404

    finally:
        pass


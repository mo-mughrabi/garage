from django.db.models import Max, Min
from django.db.models.query_utils import Q
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.template import Context
from django.template.loader import get_template
from django.conf import settings
from rest_framework import generics, status, permissions
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from serializers import *
from models import ModelLookUpI18n, Car, Image, Lookup
from forms import CarForm, ModelLookUpForm, ModelLookUpI18nForm
from garcom.misc.common_lib.models import Notification
import sys, os


class CarList(generics.ListAPIView):
    """
    API endpoint that manipulates or queries cars
    """
    model = Car
    paginate_by = 12
    serializer_class = CarSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        params = dict([(k, v) for k, v in self.request.GET.items() if v not in (None, '', u'')])

        page = params.pop('page', None)
        sort = params.pop('sort', '-created_at')
        my_vehicle = params.pop('my_vehicle', None)
        status = params.pop('status', None)

        if my_vehicle:
            params.update({
                'created_by': self.request.user,
                # override the status to return drafts
                'status__in': (Car.STATUS_ACTIVE, Car.STATUS_PENDING, Car.STATUS_SOLD, Car.STATUS_DRAFT, Car.STATUS_REJECTED)
            })

        # if no status is specified (default) -> return all Active and Sold vehicles (and users' Pending if a user is logged in)
        # if status is specified:
        #     - if it's Active or Sold -> return all Active or Sold vehicles
        #     - if it's anything else (Pending, Rejected, etc.) -> restrict vehicles for the logged in user only (unless user is staff)
        # if only logged in user vehicles are requested, return all vehicles of user
        if status is None:
            params.update({
                'status__in': (self.model.STATUS_ACTIVE, self.model.STATUS_SOLD)
            })
            if self.request.user.is_authenticated():
                queryset = Car.objects.filter(Q(status__in=Car.STATUS_PENDING, created_by=self.request.user) | Q(**params)).order_by(sort)
            else:
                queryset = Car.objects.filter(Q(**params)).order_by(sort)
        else:
            if status in (Car.STATUS_ACTIVE, Car.STATUS_SOLD):
                params.update({
                    'status': status,
                })
            else:
                if self.request.user.is_authenticated():
                    if self.request.user.is_staff:
                        params.update({
                            'status': status,
                        })
                    else:
                        params.update({
                            'status': status,
                            'created_by': self.request.user
                        })
            queryset = Car.objects.filter(**params).order_by(sort)



        return queryset

    def post(self, request, id=None, format=None):
        form = CarForm(request.DATA, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user

            # p is the flag for publish
            if request.DATA.get('status') == 'P':
                obj.status = obj.STATUS_PENDING

            obj.save()

            if obj.status == obj.STATUS_PENDING:
                # when post is published
                obj.primary_image = Image.objects.get(
                    id=request.DATA['primary_image'])
                obj.save()
                self._update_images(request, obj)
                self._send_notification(obj)

                messages.info(request, _('Your car has been successfully submitted and is currently pending approval.'))

                return Response({
                    'redirect': reverse('vehicle-index')
                })

            response = {
                'id': obj.id
            }

            return Response(response, mimetype='application/json', status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': form.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id=None, format=None):
        if request.DATA.get('status') == 'S':
            try:
                obj = Car.objects.get(id=request.DATA.get('id'), status=Car.STATUS_ACTIVE, created_by=request.user)

                obj.status = Car.STATUS_SOLD
                obj.save()

                response = {
                    'status': obj.status,
                    'status_label': obj.status_label()
                }

                return Response(response, status=status.HTTP_200_OK)
            except Car.DoesNotExist as e:
                return Response(status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                return Response({'error': u'%s' % str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id=None, format=None):
        # security check (if user is same as owner of the record)
        try:
            obj = self.model.objects.exclude(status=Car.STATUS_SOLD).get(pk=id, created_by=request.user)
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Car.DoesNotExist as e:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': u'%s' % str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _update_images(self, request, car_obj):
        # retrieve the list of uploaded images and attach them to the vehicle
        for id in request.DATA['images']:
            image = Image.objects.get(id=id)

            # uploaded image has to be created by the same user
            # creating the vehicle
            if image.created_by != request.user:
                continue

            image.car = car_obj
            image.save()


    def _send_notification(self, object):
        html = get_template('vehicle/email_template/new_vehicle.html')
        txt = get_template('vehicle/email_template/new_vehicle.txt')

        c = Context({
            'user': object.created_by.first_name,
        })

        Notification.objects.send_email(
            send_to=object.created_by.email,
            subject=_('Your car has been successfully submitted to Garage'),
            html_body=html.render(c),
            text_body=txt.render(c)
        )


class ImageDetail(APIView):
    """
    API endpoint that retrieves or creates an image.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def delete(self, request, format=None):
        try:
            im = Image.objects.get(id=request.GET.get('id', None))
            im.delete()
        except Image.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, format=None):
        params = dict([(k, v) for k, v in request.GET.items() if v not in (None, '', u'')])
        images = Image.objects.filter(**params)
        data = []
        for image in images:
            data.append({
                'created_at': image.created_at,
                'image': image.thumbnail_by_size(750, 600),
                'thumbnail': image.thumbnail
            })
        response = Response(data)
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def post(self, request, format=None):
        data = []
        for file in request.FILES.getlist('files[]'):
            obj = Image(
                car=None,
                status='D',
                created_by=request.user
            )
            obj.image.save(file.name, file)
            obj.save()

            file_name, file_ext = os.path.splitext(
                file.name.rpartition('/')[-1])
            data.append({
                'name': file.name,
                'size': file.size,
                'url': settings.MEDIA_URL + "cars/full/" + file.name,
                'thumbnail_url': obj.thumbnail_by_size(100, 100),
                'delete_url': '/vehicle/api/image.json?id=%s' % obj.id,
                'delete_type': "DELETE",
                'image_id': obj.id,
            })

        response = Response(data)
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class MakeList(APIView):
    """
    API endpoint that represents a list of makes.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = ModelLookUpI18n.objects.distinct_make(exist=request.GET.get('exist', False)).order_by('make_display')

        makes = []
        for obj in objects:
            makes.append({
                'make':    obj['model__make'],
                'display': obj['make_display'],
                'models':  reverse('model-list-api', kwargs={'make': obj['model__make']}, request=request)
            })

        return Response(makes)


class ModelDetail(APIView):
    """
    API endpoint to retrieve or create a model instance
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, make=None, model=None, trim=None, year=None, format=None):
        try:
            if trim in (None, u'', ''):
                return Response(ModelLookUpI18n.objects.values('model__id').get(
                    language=request.LANGUAGE_CODE,
                    model__make=make,
                    model__model=model,
                    model__year=year
                ))
            else:
                return Response(ModelLookUpI18n.objects.values('model__id').get(
                    language=request.LANGUAGE_CODE,
                    model__make=make,
                    model__model=model,
                    model__trim=trim,
                    model__year=year
                ))

        except ModelLookUpI18n.DoesNotExist as e:
            return Response({'error': u'No matching model'}, status=status.HTTP_404_NOT_FOUND)
        except ModelLookUpI18n.MultipleObjectsReturned as e:
            return Response({'error': u'More than one model matched'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': u'%s' % str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            base_form = ModelLookUpForm(request.DATA)

            if base_form.is_valid():
                base_obj = base_form.save(commit=False)
                base_obj.created_by = request.user

                i18n_form = ModelLookUpI18nForm(request.DATA)
                if i18n_form.is_valid():
                    # commit save if i18n passes validation
                    base_obj.save()

                    i18n_obj = i18n_form.save(commit=False)
                    i18n_obj.model = base_obj
                    i18n_obj.language = request.LANGUAGE_CODE
                    i18n_obj.save()

                    messages.info(request, _('Your model suggestion has successfully been submitted.'))

                    return Response({
                        'id': base_obj.id,
                        'redirect': reverse('vehicle-index'),
                    })
                else:
                    return Response({'error': _('Invalid i18n form data')}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': _('Invalid form data')}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': u'%s' % str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModelList(APIView):
    """
    API endpoint to query Models
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, make=None, year=None, format=None):
        objects = ModelLookUpI18n.objects.distinct_model(
            exist=request.GET.get('exist', False),
            make=make,
            year=year,
        ).values('model__model', 'model_display').order_by('model__model', 'model__year')

        models = []
        for obj in objects:
            models.append({
                'model':   obj['model__model'],
                'display': obj['model_display'],
                'trims':   reverse('trim-list-api', kwargs={'make': make, 'model': obj['model__model']}, request=request)
            })

        return Response(models)


class TrimList(APIView):
    """
    API endpoint to query Trims
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, make=None, model=None, year=None, format=None):
        objects = ModelLookUpI18n.objects.distinct_trim(
            exist=request.GET.get('exist', False),
            make=make,
            model=model,
            year=year
        ).values('model__trim', 'trim_display').order_by('model__trim')

        trims = []
        for obj in objects:
            trims.append({
                'trim':    obj['model__trim'],
                'display': obj['trim_display'],
            })

        return Response(trims)


class YearList(APIView):
    """
    API endpoint to query Years
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, make=None, model=None, trim=None, format=None):
        years = ModelLookUpI18n.objects.distinct_years(
            exist=request.GET.get('exist', False),
            make=make,
            model=model,
            trim=trim
        ).values('model__year').order_by('-model__year')

        year_min, year_max = sys.maxint, -sys.maxint - 1
        for year in (year['model__year'] for year in years):
            year_min, year_max = min(year, year_min), max(year, year_max)

        return Response({
            'yearMin': year_min,
            'yearMax': year_max,
            'years': [year['model__year'] for year in years]
        })


class ColorList(generics.ListAPIView):
    """
    API endpoint that represents a list of colors.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    model = Lookup
    serializer_class = ColorSerializer

    def get_queryset(self):
        """
        Filter the returned data
        """
        return Lookup.objects.using_translations().filter(group='COLOR').values('id', 'value').order_by('key')


class PriceRange(APIView):
    """
    API endpoint to query a range of Prices
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, make=None, model=None, trim=None, format=None):
        print make
        prices = Car.objects.filter(
            Q(asking_price__gt=0)
            & Q(model__make=make) if make is not None else Q()
            & Q(model__model=model) if model is not None else Q()
            & Q(model__trim=trim) if trim is not None else Q()
        ).aggregate(Min('asking_price'), Max('asking_price'))

        return Response({
            'min': int(prices['asking_price__min'] or 0),
            'max': int(prices['asking_price__max'] or 0)
        })


class MileageRange(APIView):
    """
    API endpoint to query a range of Mileage
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, make=None, model=None, trim=None, format=None):
        mileage = Car.objects.filter(
            Q(model__make=make) if make is not None else Q()
            & Q(model__model=model) if model is not None else Q()
            & Q(model__trim=trim) if trim is not None else Q()
        ).aggregate(Min('mileage'), Max('mileage'))

        return Response({
            'min': int(mileage['mileage__min'] or 0),
            'max': int(mileage['mileage__max'] or 0)
        })


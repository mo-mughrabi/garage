# -*- coding: utf-8 -*-
from celery.task import task
from django.conf import settings
from django.core.files import File
from django.db import transaction
from django.db.models.expressions import F
from django.db.models.loading import get_model
import os
import logging
from PIL import Image as ImageObj
from utils import watermark
from django.core.files.uploadedfile import SimpleUploadedFile
from cStringIO import StringIO
import os

logging.getLogger(__name__)



@task(name='vehicle.add_watermark', ignore_result=True)
def add_watermark(id):
    """Open original photo which we want to resize using PIL's Image object"""
    obj = get_model('vehicle', 'image').objects.get(pk=id)
    img_file = obj.image

    im = StringIO(img_file.read())
    image = ImageObj.open(im)

    # Convert to RGB if necessary
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')

    overlay = ImageObj.open(getattr(settings, 'WATERMARK_IMAGE'))
    image = watermark(image, overlay, 'bottomright', 0.4)

    temp_handle = StringIO()
    image.save(temp_handle, 'jpeg')
    temp_handle.seek(0)

    suf = SimpleUploadedFile(obj.image.name, temp_handle.read(), content_type='image/png')

    obj.image.save(obj.image.name, suf)
    obj.save()

    return True



@task(name='vehicle.add_view_count', ignore_result=True)
@transaction.commit_manually
def add_view_count(id):
    try:
        get_model('vehicle', 'car').objects.filter(
            pk=id).update(view_count=F('view_count') + 1)
        transaction.commit()
    except Exception as e:
        transaction.rollback()
        logging.error(str(e))
    finally:
        pass

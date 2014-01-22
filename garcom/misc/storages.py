from __future__ import absolute_import
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

class S3StaticBucket(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = getattr(settings, 'S3_STATIC_BUCKET_STORAGE')
        kwargs['secure_urls'] = False
        super(S3StaticBucket, self).__init__(*args, **kwargs)
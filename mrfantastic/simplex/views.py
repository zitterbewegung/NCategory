# from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets

from .models import Job
from .serializers import JobSerializer
from django.conf import settings
import boto3
import mimetypes
import json



class JobViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    API endpoint that allows jobs to be viewed or created.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer

conn = boto3.resource(s3,aws_access_key_id=settings.AWS_KEY, aws_secret_access_key=settings.AWS_SECRET)

def sign_s3_upload(request):
    object_name = request.GET['objectName']
    content_type = mimetypes.guess_type(object_name)[0]

    signed_url = conn.generate_url(
        300,
        "PUT",
        'ncategory-search-query',
        'test-query' + object_name,
        headers = {'Content-Type': content_type, 'x-amz-acl':'public-read'})

    return HttpResponse(json.dumps({'signedUrl': signed_url}))
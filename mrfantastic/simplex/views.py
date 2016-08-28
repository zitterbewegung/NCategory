# from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from .models import Job
from .serializers import JobSerializer
from django.http import HttpResponse
from rest_framework.parsers import FileUploadParser

class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format=None):
        file_obj = request.FILES['file']
        # do some stuff with uploaded file
        
        return Response("Successful upload",status=204)
   

class JobViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    API endpoint that allows jobs to be viewed or created.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    
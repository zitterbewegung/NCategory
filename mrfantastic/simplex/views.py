# from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets

from .models import Job
from .serializers import JobSerializer
from django.shortcuts import get_object_or_404
from django.shortcuts import render


class JobViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    API endpoint that allows jobs to be viewed or created.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer

def index(request):
    """
    """
    

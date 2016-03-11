from functools import wraps

from .celeryconf import app
from .models import Jo

import argparse
import base64
import httplib2

from apiclient.discovery import build
from oauth2client.client import GoogleCredentials


# decorator to avoid code duplication

def update_job(fn):
    """Decorator that will update Job with result of the function"""

    # wraps will make the name and docstring of fn available for introspection
    @wraps(fn)
    def wrapper(job_id, *args, **kwargs):
        job = Job.objects.get(id=job_id)
        job.status = 'started'
        job.save()
        try:
            # execute the function fn
            result = fn(*args, **kwargs)
            job.result = result
            job.status = 'finished'
            job.save()
        except:
            job.result = None
            job.status = 'failed'
            job.save()
    return wrapper


# two simple numerical tasks that can be computationally intensive

@app.task
@update_job
def power(n):
    """Return 2 to the n'th power"""
    return 2 ** n


@app.task
@update_job
def fib(n):
    """Return the n'th Fibonacci number.
    """
    if n < 0:
        raise ValueError("Fibonacci numbers are only defined for n >= 0.")
    return _fib(n)


def _fib(n):
    if n == 0 or n == 1:
        return n
    else:
        return _fib(n - 1) + _fib(n - 2)

@app.task
@update_job
def label_image_google_vision(photo_file):
  '''Run a label request on a single image'''

  API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'
  http = httplib2.Http()

  credentials = GoogleCredentials.get_application_default().create_scoped(
      ['https://www.googleapis.com/auth/cloud-platform'])
  credentials.authorize(http)

  service = build('vision', 'v1', http, discoveryServiceUrl=API_DISCOVERY_FILE)

  with open(photo_file, 'rb') as image:
    image_content = base64.b64encode(image.read()).decode('utf-8')
    service_request = service.images().annotate(
      body={
        'requests': [{
          'image': {
            'content': image_content
           },
          'features': [{
            'type': 'LABEL_DETECTION',
            'maxResults': 1,
           }]
         }]
      })
    response = service_request.execute()
    label = response['responses'][0]['labelAnnotations'][0]['description']
    print(('Found label: %s for %s' % (label, photo_file)))
    


@app.task
@update_job
def generate_tags(modelFile):
    """Run classifiers so that the semantic information
       of the model will be filled in to the tags field.
    """
    pass

# mapping from names to tasks

TASK_MAPPING = {
    'power': power,
    'fibonacci': fib
}

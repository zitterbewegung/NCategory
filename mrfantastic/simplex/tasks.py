from functools import wraps

from .celeryconf import app
from .models import Job
# decorator to avoid code duplication
# from .utility import convert_ply_pcd, pcd_to_vfh_histogram


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


@app.task
@update_job    
def generate_tags(modelFile):
    """Run classifiers so that the semantic information
       of the model will be filled in to the tags field.
    """

    pass


# mapping from names to tasks

TASK_MAPPING = {
    'generate_tags': generate_tags,
}

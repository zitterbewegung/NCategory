from functools import wraps

from .celeryconf import app
from .models import Job
import subprocess, tempfile
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

def generate_tags(modelFile):
    """Run classifiers so that the semantic information
       of the model will be filled in to the tags field.
    """

    pass

@app.task
def pcd_to_vfh_histogram(inputFileName, outputFileName):
    """
    
    """
    args = ['pcl_extract_feature', inputFileName, outputFileName, '-feature', 'VFHEstimation', '-n_k', '1', '-f_k', '1']
    p = subprocess.call(args)
    
    

@app.task
def convert_ply_pcd(inputFileName, outputFileName):
    with tempfile.NamedTemporaryFile(suffix='.pcd') as tf:
        args = ['pcl_obj2pcd', inputFileName, tf.name]
        tf.flush()
        p = subprocess.call(args)
        #import pdb; pdb.set_trace()
        convert_args = ['pcl_convert_pcd_ascii_binary', tf.name, outputFileName, '0']
        p2 = subprocess.call(convert_args)
        tf.flush()
        #import pdb; pdb.set_trace()
# mapping from names to tasks

TASK_MAPPING = {
    'power': power,
    'fibonacci': fib,
    'convert_ply_pcd': convert_ply_pcd,
    'generate_tags': generate_tags,
    'pcd_to_vfh_histogram': pcd_to_vfh_histogram,
}

from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from bungiesearch.managers import BungiesearchManager

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class Comment(models.Model):
    body = models.TextField()
    # author = models.ForeignKey('Account')
    print_field = models.ForeignKey('Print', models.DO_NOTHING, db_column='print')  # Field renamed because it was a Python reserved word.
    created_at = models.DateTimeField()

class Address(models.Model):
    last_name = models.TextField()
    first_name = models.TextField()
    address = models.TextField()
    address2 = models.TextField()
    city = models.TextField()
    zipcode = models.CharField(max_length=10)
    mail_state = models.TextField()
    country = models.TextField()

class Tag(models.Model):
    category = models.TextField()
    confidence = models.FloatField()


class Print(models.Model):
    title = models.TextField()
    description = models.TextField()
    file_path = models.TextField()
    image_file = models.TextField()
    thumbnail_file = models.TextField()
    print_file = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=4)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField()
    objects = BungiesearchManager()

    
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.TextField(unique=True)
    password = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()
    address = models.TextField()
    city = models.TextField()
    date_created = models.DateTimeField()
    modified_date = models.DateTimeField()
    address = models.ManyToManyField(Address)
    prints = models.ManyToManyField(Print)
    comments = models.ManyToManyField(Comment)
class PrintJob(models.Model):
    '''Created when a print has to be printed'''    
    mailing_address = models.ForeignKey(Account, on_delete=models.CASCADE)
    to_print = models.ForeignKey(Print, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
   
#Jobs class for celery
class Job(models.Model):
    """Class describing a computational job"""
 
    # currently, available types of job are:
    TYPES = (
        ('fibonacci', 'fibonacci'),
        ('power', 'power'),
    )
 
    # list of statuses that job can have
    STATUSES = (
        ('pending', 'pending'),
        ('started', 'started'),
        ('finished', 'finished'),
        ('failed', 'failed'),
    )
 
    type = models.CharField(choices=TYPES, max_length=20)
    status = models.CharField(choices=STATUSES, max_length=20)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    argument = models.PositiveIntegerField()
    result = models.IntegerField(null=True)
 
    def save(self, *args, **kwargs):
        """Save model and if job is in pending state, schedule it"""
        super(Job, self).save(*args, **kwargs)
        if self.status == 'pending':
            from .tasks import TASK_MAPPING
            task = TASK_MAPPING[self.type]
            task.delay(job_id=self.id, n=self.argument)
     
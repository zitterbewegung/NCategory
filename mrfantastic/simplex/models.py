from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from bungiesearch.managers import BungiesearchManager

from django.utils import timezone


class Comment(models.Model):
    body = models.TextField()
    # author = models.ForeignKey('Account')
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(default=timezone.now())
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

        
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
    modified_at = models.DateTimeField(default=timezone.now())
    objects = BungiesearchManager()
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Print, self).save(*args, **kwargs)

    
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.TextField(unique=True)
    password = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()
    address = models.TextField()
    city = models.TextField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(default=timezone.now())
    address = models.ManyToManyField(Address)
    prints = models.ManyToManyField(Print)
    comments = models.ManyToManyField(Comment)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Account, self).save(*args, **kwargs)


class PrintJob(models.Model):
    """Created when a print has to be printed"""
    mailing_address = models.ForeignKey(Account, on_delete=models.CASCADE)
    to_print = models.ForeignKey(Print, on_delete=models.CASCADE)
    date_created = models.DateTimeField()


class Job(models.Model):
    """Class describing a computational job for celery"""
 
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
 
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(default=timezone.now())
    argument = models.PositiveIntegerField(null=True)
    result = models.IntegerField(null=True)
 
    def save(self, *args, **kwargs):
        """Save model and if job is in pending state, schedule it"""
        super(Job, self).save(*args, **kwargs)
        if self.status == 'pending':
            from .tasks import TASK_MAPPING
            task = TASK_MAPPING[self.type]
            task.delay(job_id=self.id, n=self.argument)
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()

     
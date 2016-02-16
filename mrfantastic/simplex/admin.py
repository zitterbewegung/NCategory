from django.contrib import admin

from .models import Account, Tag, Comment, Address, Job , Print
# Register your models here.
admin.site.register(Tag)
admin.site.register(Account)
admin.site.register(Comment)
admin.site.register(Address)
admin.site.register(Print)
admin.site.register(Job)
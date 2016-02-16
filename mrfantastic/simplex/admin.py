from django.contrib import admin

from .models import Account, AccountPrint, AccountMailing, Comment, Mailing, Print
# Register your models here.
admin.site.register(Account)
admin.site.register(Comment)
admin.site.register(Mailing)
admin.site.register(Print)
admin.site.register(AccountPrint)
admin.site.register(AccountMailing)
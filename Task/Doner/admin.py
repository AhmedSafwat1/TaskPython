from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

admin.site.unregister(Group)
# Register your models here.
admin.site.register(Doner)
admin.site.register(Bank)
admin.site.register(BloodDonation)

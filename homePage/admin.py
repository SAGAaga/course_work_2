from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Accomodation)
admin.site.register(Status)
admin.site.register(Contract)
admin.site.register(Tarif)
admin.site.register(Tarif_Status)
admin.site.register(Payments)

from django.contrib import admin

# Register your models here.
from orders.models import Transport, Payment

admin.site.register(Transport)
admin.site.register(Payment)
from django.contrib import admin
from .models import SalesOrder, SalesItem

admin.site.register(SalesOrder)
admin.site.register(SalesItem)
from django.contrib import admin
from .models import Order,Products, Warehouse, Install

admin.site.register(Order)
admin.site.register(Products)
admin.site.register(Warehouse)
admin.site.register(Install)

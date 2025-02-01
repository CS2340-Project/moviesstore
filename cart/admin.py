from django.contrib import admin
from .models import Order
from .models import Item

class OrderAdmin(admin.ModelAdmin):
    ordering = ['date']

admin.site.register(Order, OrderAdmin)
admin.site.register(Item)
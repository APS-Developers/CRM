from django.contrib import admin
from .models import Inventory
from .models import Csvs
# Register your models here.
admin.site.register(Inventory)
admin.site.register(Csvs)
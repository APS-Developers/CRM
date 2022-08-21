import django_filters

from .models import *


class InventoryFilter(django_filters.FilterSet):
    class Meta:
        model = Inventory
        fields = ["Location", "Organisation"]

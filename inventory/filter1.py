import django_filters

from .models import *
class InventoryFilter(django_filters.FilterSet):
    class Meta:
        model = Inventory
        fields=['Serial_Number', 'Make', 'Part_Code', 'Item', 'Location','Organisation']
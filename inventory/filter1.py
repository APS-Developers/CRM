import django_filters
from django_filters import DateFilter
from .models import *


class InventoryFilter(django_filters.FilterSet):
    purchase_date = DateFilter(field_name="Purchase_Date")
    item_dispatch_date = DateFilter(field_name="Item_dispatched_Date")

    class Meta:
        model = Inventory
        fields = [
            "Make",
            "Part_Code",
            "Serial_Number",
            "Item",
            "Location",
            "Organisation",
            "Status",
        ]

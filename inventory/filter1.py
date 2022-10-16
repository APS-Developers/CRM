import django_filters
from django_filters import DateFilter, ChoiceFilter
from .models import *

StatusChoice = [
    ("Working", "Working"),
    ("Not Working", "Not Working"),
]


class InventoryFilter(django_filters.FilterSet):
    purchase_date = DateFilter(field_name="Purchase_Date")
    item_dispatch_date = DateFilter(field_name="Item_dispatched_Date")
    status = ChoiceFilter(choices=StatusChoice, field_name="Status")

    class Meta:
        model = Inventory
        fields = [
            "Make",
            "Part_Code",
            "Serial_Number",
            "Item",
            "Location",
            "Organisation",
        ]

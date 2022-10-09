import django_filters
from .models import *
from django_filters import DateFilter


class TicketFilter(django_filters.FilterSet):
    date_created = DateFilter(field_name="DateCreated")
    resolution_date = DateFilter(field_name="ResolutionDate")

    class Meta:
        model = Ticket
        fields = [
            "TicketID",
            "Status",
            "Priority",
            "Category",
            "SubCategory",
            "Customer__Organisation__Name",
        ]

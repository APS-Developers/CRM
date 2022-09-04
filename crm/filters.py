import django_filters
from .models import *
from django_filters import DateFilter


class TicketFilter(django_filters.FilterSet):
    date_created = DateFilter(field_name="DateCreated")
    date_closed = DateFilter(field_name="DateClosed")

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

import django_filters 
from .models import *
from django_filters import DateFilter

class TicketFilter(django_filters.FilterSet):
    date_created = DateFilter(field_name='DateCreated')

    class Meta:
        model = Ticket
        fields = ['TicketID', 'Status', 'Priority']


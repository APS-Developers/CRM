import django_filters 
from .models import *
from django_filters import DateFilter

class TicketFilter(django_filters.FilterSet):
    date_created = DateFilter(field_name='DateCreated')
    start_date = DateFilter(field_name='DateCreated', lookup_expr='gte')
    end_date = DateFilter(field_name='DateCreated', lookup_expr='lte')
    class Meta:
        model = Ticket
        fields = ['TicketID', 'Status', 'Priority']


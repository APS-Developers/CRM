import django_filters 
from .models import *

class CustomerFilter(django_filters.FilterSet):

    class Meta:
        model = Customer
        fields = ['Name', 'Organisation']


class OrganisationFilter(django_filters.FilterSet):

    class Meta:
        model = Organisation
        fields = ['Name', 'Address']
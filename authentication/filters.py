import django_filters 
from .models import *
from django.contrib.auth.models import User

class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ['id', 'username']


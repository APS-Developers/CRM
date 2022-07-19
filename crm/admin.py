from django.contrib import admin
from crm.models import Ticket
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.

admin.site.register(Ticket, SimpleHistoryAdmin) 

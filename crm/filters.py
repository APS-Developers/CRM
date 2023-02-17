import django_filters
from .models import *
from django_filters import DateFilter, ChoiceFilter

categoryChoices = [("Hardware Faulty", "Hardware Faulty")]

subCategoryChoices = [
    ("Power Issue", "Power Issue"),
    ("External Card Faulty", "External Card Faulty"),
    ("Router DRM Issue", "Router DRM Issue"),
    ("Port Faulty", "Port Faulty"),
    ("FAN not working", "FAN not working"),
    ("Power Supply Faulty", "Power Supply Faulty"),
    ("Not Booting", "Not Booting"),
    ("Unable to take Console", "Unable to take Console"),
    ("Line Card Faulty", "Line Card Faulty"),
    ("SUP Card Faulty", "SUP Card Faulty"),
    ("Physical Damage", "Physical Damage"),
]

statusChoices = [
    ("Open", "Open"),
    ("Pending", "Pending"),
    ("Resolved", "Resolved"),
    ("Closed", "Closed"),
]

priorityChoices = [("P1", "P1"), ("P2", "P2"), ("P3", "P3"), ("P4", "P4")]


class TicketFilter(django_filters.FilterSet):
    date_created = DateFilter(field_name="DateCreated")
    resolution_date = DateFilter(field_name="ResolutionDate")
    category = ChoiceFilter(choices=categoryChoices, field_name="Category")
    subCategory = ChoiceFilter(choices=subCategoryChoices, field_name="SubCategory")
    status = ChoiceFilter(choices=statusChoices, field_name="Status")
    priority = ChoiceFilter(choices=priorityChoices, field_name="Priority")

    class Meta:
        model = Ticket
        fields = [
            "TicketID",
            "Customer__Organisation__Name",
        ]

class TicketFilterReport(TicketFilter):
    date_created = DateFilter(field_name="DateCreated",lookup_expr="gt", label="Date Created From (mm/dd/yyyy)")
    to_date_created = DateFilter(field_name="DateCreated",lookup_expr="lt",label="Date Created To (mm/dd/yyyy)")
    resolution_date = DateFilter(field_name="ResolutionDate")
    category = ChoiceFilter(choices=categoryChoices, field_name="Category")
    subCategory = ChoiceFilter(choices=subCategoryChoices, field_name="SubCategory")
    status = ChoiceFilter(choices=statusChoices, field_name="Status")
    priority = ChoiceFilter(choices=priorityChoices, field_name="Priority")

    class Meta:
        model = Ticket
        fields = [
            "TicketID",
            "Customer__Organisation__Name",
            "date_created",
            "to_date_created",
        ]
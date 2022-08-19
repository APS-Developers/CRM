import django
from django.db import models
from customer.models import Customer
from inventory.models import Inventory
from simple_history.models import HistoricalRecords

# Create your models here.

class Ticket(models.Model):

    class Meta:
        db_table = "Ticket"

    priorityChoices = [
        ("P1", "P1"),
        ("P2", "P2"),
        ("P3", "P3"),
        ("P4", "P4")
    ]
    boolChoices = [(True, 'Yes'), (False, 'No')]
    statusChoices = [
        ("Open", "Open"),
        ("Resolved", "Resolved"),
        ("Pending", "Pending"),
        ("Closed", "Closed")
    ]
    faultChoices = [
        ("Router", "Router faulty"),
        ("Modem", "Modem faulty"),
        ("Switch", "Switch faulty")
    ]
    resolutionChoices = [
        ("123", "Router faulty"),
        ("456", "Modem faulty")
    ]

    TicketID = models.AutoField('Ticket ID', primary_key=True)
    DateCreated = models.DateField('Date Created', default=django.utils.timezone.now)
    Category = models.CharField(max_length=100)
    SubCategory = models.CharField('Sub-Category', max_length=100)
    ModelNo = models.CharField('Model No', max_length=100)
    SerialNo = models.CharField('Serial No', max_length=100)
    Summary = models.TextField(max_length=500, blank=True)
    Priority = models.CharField(max_length=2, choices=priorityChoices, blank=True)
    AMC = models.BooleanField(choices=boolChoices, null=True)
    Status = models.CharField(choices=statusChoices, max_length=10, blank=True)
    FaultFoundCode = models.CharField('Fault Found Code', choices=faultChoices, max_length=30, blank=True)
    ResolutionCode = models.CharField('Resolution Code', choices=resolutionChoices, max_length=20, blank=True)
    ResolutionRemarks = models.TextField('Resolution Remarks', max_length=500, blank=True)
    Customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, null=True)
    OnlineResolvable = models.BooleanField('Can it be resolved online?', choices=boolChoices, null=True)
    AlternateHW = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING, blank=True, null=True) 
    history = HistoricalRecords()

    def __str__(self):
        return str(self.TicketID)

    # customer hoga foreign key
    # Organisation = models.CharField(max_length=100)     # drop down , auto-populate also editable
    # CustomerName = models.CharField('Customer Name', max_length=100)
    # ContactNo = PhoneNumberField('Contact No')
    # EmailAddress = models.EmailField('Email Address', max_length=200, blank=True)

# organisation table -> name, pta, id, email, location, contact,
# customer table -> id, CustomerName, ContactNo, EmailAddress, org id by the name of org - foreign key

# django, get create
# reverse lookup - one to many

# nupur ko dena hai id aur naam
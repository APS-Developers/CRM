import django
from django.db import models
from customer.models import Customer
from inventory.models import Inventory
from simple_history.models import HistoricalRecords
import datetime

# Create your models here.
SLA_TIME = {
    "P1": datetime.timedelta(hours=72),
    "P2": datetime.timedelta(hours=72),
    "P3": datetime.timedelta(hours=72),
    "P4": datetime.timedelta(hours=72),
}


class Ticket(models.Model):
    class Meta:
        db_table = "Ticket"

    priorityChoices = [("P1", "P1"), ("P2", "P2"), ("P3", "P3"), ("P4", "P4")]
    boolChoices = [("", "---------"), ("Yes", "Yes"), ("No", "No")]
    statusChoices = [
        ("Open", "Open"),
        ("Pending", "Pending"),
        ("Resolved", "Resolved"),
        ("Closed", "Closed"),
    ]
    resolutionChoices = [
        ("", "---------"),
        (
            "Power Issue Resolved with Hard Reset",
            "Power Issue Resolved with Hard Reset",
        ),
        ("External Card Dispatched", "External Card Dispatched"),
        ("DRM Issue Resolved", "DRM Issue Resolved"),
        ("New Hardware Dispatched", "New Hardware Dispatched"),
        ("FAN/Module Dispatched", "FAN/Module Dispatched"),
        ("Power Supply Replaced/Dispatched", "Power Supply Replaced/Dispatched"),
        ("Booting Issue Resolved", "Booting Issue Resolved"),
        ("Console Issues Resolved", "Console Issues Resolved"),
        ("Line Card Replaced/Dispatched", "Line Card Replaced/Dispatched"),
        ("SUP Card Replaced/Dispatched", "SUP Card Replaced/Dispatched"),
        (
            "Physical Damage - Not covered in AMC",
            "Physical Damage - Not covered in AMC",
        ),
        ("Others", "Others"),
    ]
    dispatchedChoices = [
        ("", "---------"),
        ("DTDC", "DTDC"),
        ("BLUEDART", "BLUEDART"),
        ("MARUTI", "MARUTI"),
        ("DELHIVERY", "DELHIVERY"),
        ("SAFEXPRESS", "SAFEXPRESS"),
        ("GATI", "GATI"),
    ]
    deliveryStatus = [
        ("", "---------"),
        ("Dispatched", "Dispatched"),
        ("In Transit", "In Transit"),
        ("Out for Delivery", "Out for Delivery"),
        ("Delivered", "Delivered"),
    ]

    TicketID = models.AutoField("Ticket ID", primary_key=True)
    DateCreated = models.DateField(
        "Date Created (mm/dd/yyyy)", default=django.utils.timezone.now
    )
    Category = models.CharField(max_length=100)
    SubCategory = models.CharField("Sub-Category", max_length=100)
    SerialNo = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING)
    Summary = models.TextField(max_length=500, blank=True)
    Priority = models.CharField(max_length=2, choices=priorityChoices, blank=True)
    Status = models.CharField(choices=statusChoices, max_length=10, blank=True)
    FaultFoundCode = models.CharField("Fault Found Code", max_length=100, blank=True)
    ResolutionCode = models.CharField(
        "Resolution Code", choices=resolutionChoices, max_length=100, blank=True
    )
    ResolutionRemarks = models.TextField(
        "Resolution Remarks", max_length=500, blank=True
    )
    Customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, null=True)
    OnlineResolvable = models.CharField(
        "Online Resolvable", choices=boolChoices, blank=True, max_length=10
    )
    HWDispatched = models.ForeignKey(
        Inventory,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="replacement",
    )
    ResolutionDate = models.DateField(
        "Resolution Date (mm/dd/yyyy)", null=True, blank=True
    )
    DocketNumber = models.CharField("Docket Number", max_length=50, blank=True)
    DispatchedThrough = models.CharField(
        "Dispatched through", choices=dispatchedChoices, blank=True, max_length=50
    )
    DeliveryStatus = models.CharField(
        "Delivery Status", choices=deliveryStatus, blank=True, max_length=30
    )
    Notes = models.TextField(max_length=500, blank=True)
    ClosureDate = models.DateField(
        "Closure Date (mm/dd/yyyy)", null=True, blank=True
    )
    ClosureRemarks = models.TextField(
        "Closure Remarks", max_length=500, blank=True
    )

    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    @property
    def sla_status(self):
        if self.Status == "Closed":
            if (self.ResolutionDate - self.DateCreated) > SLA_TIME[self.Priority]:
                return "outside"
            else:
                return "within"
        else:
            if (datetime.datetime.now().date() - self.DateCreated) > SLA_TIME[
                self.Priority
            ]:
                return "outside"
            else:
                return "within"

    def __str__(self):
        return str(self.TicketID)

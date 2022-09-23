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
    boolChoices = [(True, "Yes"), (False, "No")]
    statusChoices = [
        ("Open", "Open"),
        ("Resolved", "Resolved"),
        ("Pending", "Pending"),
        ("Closed", "Closed"),
    ]
    faultChoices = [
        ("Router", "Router faulty"),
        ("Modem", "Modem faulty"),
        ("Switch", "Switch faulty"),
    ]
    resolutionChoices = [("123", "Router faulty"), ("456", "Modem faulty")]

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
    FaultFoundCode = models.CharField(
        "Fault Found Code", choices=faultChoices, max_length=30, blank=True
    )
    ResolutionCode = models.CharField(
        "Resolution Code", choices=resolutionChoices, max_length=20, blank=True
    )
    ResolutionRemarks = models.TextField(
        "Resolution Remarks", max_length=500, blank=True
    )
    Customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, null=True)
    OnlineResolvable = models.BooleanField(
        "Can it be resolved online?", choices=boolChoices, null=True
    )
    AlternateHW = models.ForeignKey(
        Inventory,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="replacement",
    )
    DateClosed = models.DateField("Date Closed (mm/dd/yyyy)", null=True, blank=True)
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
            if (self.DateClosed - self.DateCreated) > SLA_TIME[self.Priority]:
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

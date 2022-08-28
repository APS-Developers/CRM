from django.db import models
from .validators import validate_file_extension
from datetime import datetime
from customer.models import Organisation


class Inventory(models.Model):
    class Meta:
        db_table = "Inventory"

    StatusChoice = [("None", "None"), ("Working", "Working"), ("Not Working", "Not Working")]

    Make = models.CharField(max_length=50)
    Part_Code = models.CharField(max_length=100)
    Serial_Number = models.TextField(primary_key=True)
    Item = models.CharField(max_length=50)
    Location = models.TextField()
    Purchase_Date = models.DateField(default=datetime.now, null=True)
    Item_dispatched_Date = models.DateField(null=True)
    Organisation = models.ForeignKey(
        Organisation, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    Status = models.CharField(
        choices=StatusChoice, max_length=20, blank=True, null=True
    )
    Slip = models.FileField(
        upload_to="", validators=[validate_file_extension], null=True, blank=True
    )

    def __str__(self):
        return self.Serial_Number


class Csvs(models.Model):
    file_name = models.FileField(upload_to="csvs")
    upload_date = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"

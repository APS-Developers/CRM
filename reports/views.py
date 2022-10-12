from django.shortcuts import render
from inventory.filter1 import InventoryFilter
from inventory.models import Inventory
from django.http import HttpResponse
import csv
from crm.models import Ticket
from crm.filters import TicketFilter

# Create your views here.
def dashboard(request):
    return render(request, "reports/reports_dashboard.html")


def inventory_report(request):
    if request.method == "POST":
        all_inventory = Inventory.objects.all().order_by("-Serial_Number")
        inventory_filter = InventoryFilter(request.POST, all_inventory)
        rows = inventory_filter.qs
        fields = [
            "Make",
            "Part_Code",
            "Serial_Number",
            "Item",
            "Location",
            "Purchase_Date",
            "Item_dispatched_Date",
            "Organisation",
            "Status",
            "CLI_snapshot",
            "Snapshot_Date",
        ]
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="report.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(fields)
        for row in rows:
            writer.writerow([str(getattr(row, field)) for field in fields])
        return response
    else:
        inventory_filter = InventoryFilter()
        return render(
            request, "reports/report_form.html", {"form": inventory_filter.form}
        )


def crm_report(request):
    if request.method == "POST":
        all_tickets = Ticket.objects.all().order_by("-DateCreated")
        tickets_filter = TicketFilter(request.POST, all_tickets)
        rows = tickets_filter.qs
        fields = [
            "TicketID",
            "DateCreated",
            "Category",
            "SubCategory",
            "SerialNo",
            "Summary",
            "Priority",
            "Status",
            "FaultFoundCode",
            "ResolutionCode",
            "ResolutionRemarks",
            "Customer",
            "OnlineResolvable",
            "HWDispatched",
            "ResolutionDate",
            "DocketNumber",
            "DispatchedThrough",
            "DeliveryStatus",
        ]
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="report.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(fields)
        for row in rows:
            writer.writerow([str(getattr(row, field)) for field in fields])
        return response
    else:
        tickets_filter = TicketFilter()
        return render(
            request, "reports/report_form.html", {"form": tickets_filter.form}
        )

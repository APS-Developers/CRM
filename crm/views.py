from django.shortcuts import redirect, render
from .models import Ticket
from customer.models import Customer
from .forms import CustomerForm, ProductForm, CreateTicketForm, UpdateForm
from .filters import TicketFilter
from django.contrib import messages
from inventory.models import Inventory
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from authentication.models import User, UserPermission
from django.views.decorators.cache import never_cache
from datetime import datetime
from django.http import JsonResponse
from django.core.paginator import Paginator
import datetime
import traceback

# Create your views here.


def crmPermission(user):
    if not user.is_staff or not user.is_superuser:
        permission = UserPermission.objects.get(user_id=user.id).CRM_permission
    if user.is_staff or user.is_superuser or permission:
        return True
    else:
        return False


@login_required(login_url="login")
def customerDetails(request):
    if crmPermission(request.user):
        form = CustomerForm()
        if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
                customerForm = form.save(commit=False)
                customer = Customer.objects.filter(
                    ContactNo=form.cleaned_data.get("ContactNo"),
                    Organisation=form.cleaned_data.get("Organisation"),
                    Name=form.cleaned_data.get("Name"),
                    EmailAddress=form.cleaned_data.get("EmailAddress"),
                )

                if not customer.exists():
                    allContactNos = list(
                        Customer.objects.values("ContactNo").distinct()
                    )
                    for i in range(len(allContactNos)):
                        if (
                            form.cleaned_data.get("ContactNo")
                            == allContactNos[i]["ContactNo"]
                        ):
                            messages.error(
                                request,
                                "Customer with this contact number already exists!",
                            )
                            return redirect("customerDetails")

                    customerForm.save()
                    return redirect("/productDetails/" + str(customerForm.CustomerID))

                return redirect("/productDetails/" + str(customer[0].CustomerID))
        context = {"form": form, "type": "Customer"}
        return render(request, "crm/create.html", context)
    else:
        raise PermissionDenied


@login_required(login_url="login")
def productDetails(request, customerID):
    if crmPermission(request.user):
        form = ProductForm()
        if request.method == "POST":
            form = ProductForm(request.POST)
            if form.is_valid():
                newTicket = form.save(commit=False)
                newTicket.Customer_id = customerID
                newTicket.Status = "Open"
                newTicket.save()

                orgID = Customer.objects.get(CustomerID=customerID).Organisation_id
                allProducts = list(
                    Inventory.objects.filter(Organisation_id=orgID).values(
                        "Serial_Number"
                    )
                )
                productSNo = []
                for i in range(len(allProducts)):
                    productSNo.append(allProducts[i]["Serial_Number"])

                if newTicket.SerialNo not in productSNo:
                    newTicket.Status = "Pending"
                    newTicket.AMC = False
                    newTicket.save()
                    return redirect("showTicket")

                newTicket.AMC = True
                newTicket.save()
                return redirect("/faultDetails/" + str(newTicket.TicketID))
        context = {"form": form, "type": "Product"}
        return render(request, "crm/create.html", context)
    else:
        raise PermissionDenied


@login_required(login_url="login")
def faultDetails(request, ticketID):
    if crmPermission(request.user):
        form = FaultForm()
        if request.method == "POST":
            form = FaultForm(request.POST)
            if form.is_valid():
                fault = form.save(commit=False)
                ticket = Ticket.objects.get(TicketID=ticketID)
                ticket.Priority = fault.Priority
                ticket.FaultFoundCode = fault.FaultFoundCode
                ticket.ResolutionCode = fault.ResolutionCode
                ticket.ResolutionRemarks = fault.ResolutionRemarks
                ticket.OnlineResolvable = fault.OnlineResolvable
                ticket.Summary = fault.Summary
                ticket.save()
                return redirect("showTicket")
        context = {"form": form, "type": "Fault"}
        return render(request, "crm/create.html", context)
    else:
        raise PermissionDenied


@login_required(login_url="login")
def createTicketValidate(request):
    if crmPermission(request.user):
        if not request.GET.get("serial"):
            return render(request, "crm/serial_search.html")
        else:
            try:
                product = Inventory.objects.get(Serial_Number=request.GET.get("serial"))
                if product.Organisation is None:
                    messages.add_message(request, messages.ERROR, "Product not sold!")
                    return render(request, "crm/serial_search.html")
                elif product.Item_dispatched_Date is None:
                    messages.add_message(
                        request, messages.ERROR, "Product not delivered!"
                    )
                    return render(request, "crm/serial_search.html")
                else:
                    return redirect(
                        "createTicket", product_Serial_Number=product.Serial_Number
                    )
            except Exception as e:
                messages.add_message(request, messages.ERROR, "Product not found!")
                return render(request, "crm/serial_search.html")
    else:
        raise PermissionDenied


@login_required(login_url="login")
def createTicket(request, product_Serial_Number):
    if crmPermission(request.user):
        product = Inventory.objects.get(Serial_Number=product_Serial_Number)
        if request.method == "POST":
            ticket_form = CreateTicketForm(request.POST)
            if ticket_form.is_valid():
                try:
                    newTicket = ticket_form.save(commit=False)
                    if request.POST.get("customer_id"):
                        newTicket.Customer_id = request.POST.get("customer_id")
                    else:
                        customer = CustomerForm(request.POST)
                        if customer.is_valid():
                            customer = customer.save()
                        else:
                            for error in customer.errors.values():
                                messages.add_message(
                                    request, messages.ERROR, error.as_text()
                                )
                            return render(
                                request,
                                "crm/form.html",
                                {
                                    "product": product,
                                    "form": ticket_form,
                                    "customer": customer,
                                },
                            )
                        newTicket.Customer = customer
                    newTicket.Status = "Open"
                    newTicket.ResolutionCode = ""
                    newTicket.DispatchedThrough = ""
                    newTicket.DeliveryStatus = ""
                    newTicket.OnlineResolvable = ""
                    newTicket.save()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        'Ticket "%s" created successfully!' % newTicket.TicketID,
                    )
                    return redirect("showTicket")
                except Exception as e:
                    messages.add_message(request, messages.ERROR, str(e))
                    return render(request, "crm/form.html")
            else:
                messages.add_message(
                    request, messages.ERROR, "Please fill all the fields!"
                )
                return render(request, "crm/form.html")
        else:
            ticket_form = CreateTicketForm()
            customer_form = CustomerForm()
            return render(
                request,
                "crm/form.html",
                {"product": product, "form": ticket_form, "customer": customer_form},
            )
    else:
        raise PermissionDenied


@login_required(login_url="login")
def showTicket(request):
    if crmPermission(request.user):
        all_tickets = Ticket.objects.all().order_by("-DateCreated","-TicketID")
        ticket_filter = TicketFilter(request.GET, queryset=all_tickets)
        all_tickets = ticket_filter.qs
        page_number = request.GET.get("page", 1)
        paginator = Paginator(all_tickets, 25)
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        counter = range(page_obj.start_index(), page_obj.end_index() + 1)
        for ctr, item in zip(counter, page_obj.object_list):
            item.counter = ctr
        context = {
            "page_obj": page_obj,
            "ticket_filter": ticket_filter,
            "type": "Ticket",
            "page_range": page_range,
        }
        return render(request, "crm/show.html", context)
    else:
        raise PermissionDenied


@login_required(login_url="login")
def updateTicket(request, ticketID):
    if crmPermission(request.user):
        ticket = Ticket.objects.get(TicketID=ticketID)
        form = UpdateForm(instance=ticket)
        all_history = list(ticket.history.all())
        if request.method == "POST":
            try:
                ticket_status = ticket.Status
                form = UpdateForm(request.POST, instance=ticket)
                if form.is_valid():
                    update = form.save(commit=False)
                    if "HWDispatched" in form.changed_data:
                        try:
                            HWDispatched = update.HWDispatched
                            HWDispatched.Item_dispatched_Date = datetime.datetime.now()
                            HWDispatched.Organisation = ticket.Customer.Organisation
                            HWDispatched.save()
                        except Exception as e:
                            raise Exception(
                                "Invalid Serial Number for Hardware Dispatched"
                            )

                    update.save()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        'Ticket "%s" updated successfully!' % ticketID,
                    )
                    return redirect("showTicket")
                else:
                    for error in form.errors.values():
                        messages.add_message(request, messages.ERROR, error)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))

        events = []

        dict = {
            "Status": "",
            "FaultFoundCode": "",
            "ResolutionCode": "",
            "ResolutionRemark": "",
            "HW Dispatched": "",
            "OnlineResolvable": "",
            "Notes": "",
        }
        resolutionMap = {1: "Yes", 0: "N", None: "Unknown"}

        for history in reversed(all_history):
            if history.history_type == "+":
                events.append(
                    {
                        "type": "Created",
                        "time": history.history_date,
                        "user": history.history_user,
                    }
                )

            else:
                event = {
                    "type": "Updated",
                    "time": history.history_date,
                    "user": history.history_user,
                }
                updates = {}
                if history.Status != dict["Status"]:
                    updates["Status"] = history.Status
                if history.ResolutionCode != dict["ResolutionCode"]:
                    updates["ResolutionCode"] = history.ResolutionCode
                if history.FaultFoundCode != dict["FaultFoundCode"]:
                    updates["FaultFoundCode"] = history.FaultFoundCode
                if history.ResolutionRemarks != dict["ResolutionRemark"]:
                    updates["ResolutionRemark"] = history.ResolutionRemarks
                if history.HWDispatched != dict["HW Dispatched"]:
                    updates["HW Dispatched"] = history.HWDispatched

                if history.Notes != dict["Notes"]:
                    updates["Notes"] = history.Notes

                if history.OnlineResolvable != dict["OnlineResolvable"]:
                    if history.OnlineResolvable == True:
                        updates["OnlineResolvable"] = "Yes"
                    if history.OnlineResolvable == False:
                        updates["OnlineResolvable"] = "No"
                    if history.OnlineResolvable == None:
                        updates["OnlineResolvable"] = "Unknown"
                    #  resolutionMap[history.OnlineResolvable]
                if len(updates) != 0:
                    event["updates"] = updates
                    events.append(event)
            dict["Status"] = history.Status
            dict["ResolutionCode"] = history.ResolutionCode
            dict["FaultFoundCode"] = history.FaultFoundCode
            dict["ResolutionRemark"] = history.ResolutionRemarks
            dict["HW Dispatched"] = history.HWDispatched
            dict["OnlineResolvable"] = history.OnlineResolvable
            dict["Notes"] = history.Notes
        context = {"form": form, "events": events}
        return render(request, "crm/update.html", context)
    else:
        raise PermissionDenied


# @login_required(login_url="login")
# def deleteTicket(request, ticketID):
#     if crmPermission(request.user):
#         ticket = Ticket.objects.get(TicketID=ticketID)

#         if request.method == "POST":
#             ticket.delete()
#             return redirect("showTicket")

#         context = {"ticket": ticket}
#         return render(request, "crm/delete.html", context)
#     else:
#         raise PermissionDenied


@login_required(login_url="login")
def ticketLog(request, ticketID):
    if request.user.is_staff or request.user.is_superuser:
        ticket = Ticket.objects.get(TicketID=ticketID)

        all_history = list(ticket.history.all())
        context = {"ticket": ticket, "type": "History", "all_history": all_history}
        return render(request, "crm/show.html", context)

    else:
        raise PermissionDenied


@never_cache
@login_required(login_url="login")
def dashboard(request):
    tickets = Ticket.objects.values("Status", "Priority")
    status_count = dict()
    priority_count = dict()
    for status, _ in Ticket.statusChoices:
        status_count[status] = 0
    for priority, _ in Ticket.priorityChoices:
        priority_count[priority] = 0
    for ticket in tickets:
        status = ticket["Status"]
        priority = ticket["Priority"]
        if status in status_count.keys():
            status_count[status] += 1
        if priority in priority_count.keys():
            priority_count[priority] += 1
    context = {"status_count": status_count, "priority_count": priority_count}
    return render(request, "crm/dashboard.html", context)


@login_required(login_url="login")
def getTicketSla(request):
    try:
        sla_time = datetime.datetime.now() - datetime.timedelta(days=6 * 30)
        tickets = Ticket.objects.filter(DateCreated__gte=sla_time)
        tickets_within_sla = 0
        total_tickets = tickets.count()
        for ticket in tickets:
            if ticket.sla_status == "within":
                tickets_within_sla += 1
        return JsonResponse(
            {
                "within": tickets_within_sla,
                "total": total_tickets,
                "outside": total_tickets - tickets_within_sla,
            },
            status=200,
        )
    except Exception as e:
        return JsonResponse(
            {"Error": "Internal Server Error", "description": str(e)}, status=500
        )


@login_required(login_url="login")
def getTicketSlaMonthly(request):
    try:
        total = []
        within = []
        outside = []
        months = []
        MONTH = {
            1: "JAN",
            2: "FEB",
            3: "MAR",
            4: "APR",
            5: "MAY",
            6: "JUN",
            7: "JUL",
            8: "AUG",
            9: "SEP",
            10: "OCT",
            11: "NOV",
            12: "DEC",
        }
        for i in range(5, -1, -1):
            sla_start = datetime.datetime.now() - datetime.timedelta(days=(i + 1) * 30)
            sla_end = datetime.datetime.now() - datetime.timedelta(days=i * 30)
            tickets = Ticket.objects.filter(
                DateCreated__gte=sla_start, DateCreated__lte=sla_end
            )
            tickets_within_sla = 0
            total_tickets = tickets.count()
            for ticket in tickets:
                if ticket.sla_status == "within":
                    tickets_within_sla += 1
            within.append(tickets_within_sla)
            total.append(total_tickets)
            outside.append(total_tickets - tickets_within_sla)
            months.append(f"{MONTH[sla_start.month]}-{MONTH[sla_end.month]}")
        return JsonResponse(
            {"within": within, "total": total, "outside": outside, "months": months},
            status=200,
        )
    except Exception as e:
        return JsonResponse(
            {"Error": "Internal Server Error", "description": str(e)}, status=500
        )

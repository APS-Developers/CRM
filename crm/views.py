from django.shortcuts import redirect, render
from .models import Ticket
from customer.models import Customer
from .forms import CustomerForm, ProductForm, FaultForm, UpdateForm
from .filters import TicketFilter
from django.contrib import messages
from inventory.models import Inventory
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from authentication.models import User, UserPermission
from django.views.decorators.cache import never_cache
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.core.paginator import Paginator
import datetime
from customer.forms import CreateCustomerForm

# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string

# Create your views here.


def crmPermission(username):
    user = User.objects.get(username=username)
    if not user.is_staff or not user.is_superuser:
        permission = UserPermission.objects.get(user_id=user.id).CRM_permission
    if user.is_staff or user.is_superuser or permission:
        return True
    else:
        return False


@login_required(login_url="login")
def customerDetails(request):
    if crmPermission(request.user.username):
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
    if crmPermission(request.user.username):
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
    if crmPermission(request.user.username):
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
def createTicket(request):
    if crmPermission(request.user.username):
        form = FaultForm()
        if request.method == "POST":
            form = FaultForm(request.POST)
            if form.is_valid():
                try:
                    newTicket = form.save(commit=False)
                    if request.POST.get("customer_id"):
                        newTicket.Customer_id = request.POST.get("customer_id")
                    else:
                        customer = CustomerForm(request.POST)
                        if customer.is_valid():
                            customer = customer.save()
                        else:
                            print(customer.errors)
                            raise Exception("Invalid Customer details")
                        newTicket.Customer = customer
                    newTicket.Status = "Open"
                    newTicket.save()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        'Ticket "%s" created successfully!' % newTicket.TicketID,
                    )
                    return redirect("showTicket")
                except Exception as e:
                    messages.add_message(request, messages.ERROR, "Error in creating ticket!")
                    return render(request, "crm/form.html")
            else:
                messages.add_message(
                    request, messages.ERROR, "Please fill all the fields!"
                )
                return render(request, "crm/form.html")
        return render(request, "crm/form.html")
    else:
        raise PermissionDenied


@login_required(login_url="login")
def showTicket(request):
    if crmPermission(request.user.username):
        all_tickets = Ticket.objects.all().order_by("-DateCreated")
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
    if crmPermission(request.user.username):
        ticket = Ticket.objects.get(TicketID=ticketID)
        form = UpdateForm(instance=ticket)

        if request.method == "POST":
            form = UpdateForm(request.POST, instance=ticket)
            if form.is_valid():
                update = form.save(commit=False)
                if update.Status == "Closed":
                    date = datetime.date.today()
                    update.ResolutionDate = date
                else:
                    update.ResolutionDate = None
                update.save()
                return redirect("showTicket")

        context = {"form": form}
        return render(request, "crm/update.html", context)
    else:
        raise PermissionDenied


@login_required(login_url="login")
def deleteTicket(request, ticketID):
    if crmPermission(request.user.username):
        ticket = Ticket.objects.get(TicketID=ticketID)

        if request.method == "POST":
            ticket.delete()
            return redirect("showTicket")

        context = {"ticket": ticket}
        return render(request, "crm/delete.html", context)
    else:
        raise PermissionDenied


@login_required(login_url="login")
def ticketLog(request, ticketID):
    if request.user.username == "admin":
        ticket = Ticket.objects.get(TicketID=ticketID)

        all_history = list(ticket.history.all())
        # history_users = []
        # for i in range(len(all_history)):
        #     history_users.append(User.objects.get(id=all_history[i].history_user_id).username)

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
            0: "JAN",
            1: "FEB",
            2: "MAR",
            3: "APR",
            4: "MAY",
            5: "JUN",
            6: "JUL",
            7: "AUG",
            8: "SEP",
            9: "OCT",
            10: "NOV",
            11: "DEC",
        }
        for i in range(6):
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

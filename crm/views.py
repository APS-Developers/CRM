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
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string

# Create your views here.


def crmPermission(username):
    user = User.objects.get(username=username)
    if not user.is_staff or not user.is_superuser:
        permission = UserPermission.objects.get(user_id=user.id).CRM_permission
        return permission
    return True


@login_required(login_url='login')
def customerDetails(request):
    if crmPermission(request.user.username):
        form = CustomerForm()
        if request.method == 'POST':
            form = CustomerForm(request.POST)
            if form.is_valid():
                customerForm = form.save(commit=False)
                customer = Customer.objects.filter(ContactNo=form.cleaned_data.get('ContactNo'),
                Organisation=form.cleaned_data.get('Organisation'), 
                Name=form.cleaned_data.get('Name'), 
                EmailAddress=form.cleaned_data.get('EmailAddress'))

                if not customer.exists():
                    allContactNos = list(Customer.objects.values('ContactNo').distinct())
                    for i in range(len(allContactNos)):
                        if form.cleaned_data.get('ContactNo') == allContactNos[i]['ContactNo']:
                            messages.error(request, 'Customer with this contact number already exists!')
                            return redirect('customerDetails')

                    customerForm.save()
                    return redirect('/productDetails/' + str(customerForm.CustomerID))
                
                return redirect('/productDetails/' + str(customer[0].CustomerID))
        context = {'form': form, 'type': 'Customer'}
        return render(request, 'crm/create.html', context)
    else:
        raise PermissionDenied


@login_required(login_url='login')
def productDetails(request, customerID):
    if crmPermission(request.user.username):
        form = ProductForm()
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                newTicket = form.save(commit=False)
                newTicket.Customer_id = customerID
                newTicket.Status = 'Open'
                newTicket.save()

                orgID = Customer.objects.get(CustomerID=customerID).Organisation_id
                allProducts = list(Inventory.objects.filter(Organisation_id=orgID).values('Serial_Number'))
                productSNo = []
                for i in range(len(allProducts)):
                    productSNo.append(allProducts[i]['Serial_Number'])

                if newTicket.SerialNo not in productSNo:
                    newTicket.Status = 'Pending'
                    newTicket.AMC = False
                    newTicket.save()
                    return redirect('showTicket')
                
                newTicket.AMC = True
                newTicket.save()
                return redirect('/faultDetails/' + str(newTicket.TicketID))
        context = {'form': form, 'type': 'Product'}
        return render(request, 'crm/create.html', context)
    else:
        raise PermissionDenied


@login_required(login_url='login')
def createTicket(request):
    if crmPermission(request.user.username):
        form = FaultForm()
        if request.method == 'POST':
            form = FaultForm(request.POST)
            if form.is_valid():
                newTicket = form.save(commit=False)
                if request.POST.get("customer_id"):
                    newTicket.Customer_id = request.POST.get("customer_id")
                else:
                    customer = Customer(Name=request.POST["name"],EmailAddress=request.POST["email"],ContactNo=request.POST["phone"],Organisation_id=request.POST["organisation_id"])
                    customer.save()
                    newTicket.Customer = customer
                newTicket.save()
                messages.add_message(request, messages.SUCCESS, 'Ticket "%s" created successfully!'%newTicket.TicketID)
                return redirect('showTicket')
            else:
                messages.add_message(request, messages.ERROR, 'Please fill all the fields!')
                return render(request,'crm/form.html')
        return render(request, 'crm/form.html')
    else:
        raise PermissionDenied


@login_required(login_url='login')
def showTicket(request):
    if crmPermission(request.user.username):
        all_tickets = Ticket.objects.all()
        ticket_filter = TicketFilter(request.GET, queryset=all_tickets)
        all_tickets = ticket_filter.qs
        context = {'all_tickets': all_tickets, 'ticket_filter': ticket_filter, 'type': 'Ticket'}
        return render(request, 'crm/show.html', context)
    else:     
        raise PermissionDenied


@login_required(login_url='login')
def updateTicket(request, ticketID):
    if crmPermission(request.user.username):
        ticket = Ticket.objects.get(TicketID=ticketID)
        form = UpdateForm(instance=ticket)

        if request.method == 'POST':
            form = UpdateForm(request.POST, instance=ticket)
            if form.is_valid():
                updates = form.save(commit=False)
                serialNo = updates.AlternateHW
                if serialNo is not None:
                    product = Inventory.objects.get(Serial_Number=serialNo)
                    product.Organisation_id = updates.Customer.Organisation_id
                    product.save()
                updates.save()
                return redirect('showTicket')
                
        context = {'form': form}
        return render(request, 'crm/update.html', context)
    else:
        raise PermissionDenied


@login_required(login_url='login')
def ticketLog(request, ticketID):
    if request.user.username == 'admin':
        ticket = Ticket.objects.get(TicketID=ticketID)

        all_history = list(ticket.history.all())

        # history_users = []
        # for i in range(len(all_history)):
        #     history_users.append(User.objects.get(id=all_history[i].history_user_id).username)

        context = {'ticket': ticket, 'type': 'History', 'all_history': all_history}
        return render(request, 'crm/show.html', context)

    else:
        raise PermissionDenied

    # show ticket ka nme se kia , int str se farak?
    # autofill, contact vala, 
    # .models matlab sare models ?
    # table me next ka option

def priority(request, noDays):

    p1Tickets = Ticket.objects.filter(DateCreated__lte=timezone.now() - timedelta(days=noDays), Priority="P1")
    p2Tickets = Ticket.objects.filter(priority="P2")
    p3Tickets = Ticket.objects.filter(priority="P3")
    p4Tickets = Ticket.objects.filter(priority="P4")
    context = {'p1Tickets': p1Tickets, 'p2Tickets': p2Tickets, 'p3Tickets': p3Tickets, 'p4Tickets': p4Tickets}
    return render(request, 'crm/show.html', context)

# priority, sla (72 hrs), status, -> past 1 week and 1 month, 
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
def faultDetails(request, ticketID):
    if crmPermission(request.user.username):
        form = FaultForm()
        if request.method == 'POST':
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
                return redirect('showTicket')
        context = {'form': form, 'type': 'Fault'}
        return render(request, 'crm/create.html', context)
    else:
        raise PermissionDenied


@login_required(login_url='login')
def showTicket(request):
    if crmPermission(request.user.username):
        all_tickets = Ticket.objects.all()
        ticket_filter = TicketFilter(request.GET, queryset=all_tickets)
        all_tickets = ticket_filter.qs
        context = {'all_tickets': all_tickets, 'ticket_filter': ticket_filter,'type':'Ticket'}
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
                form.save()
                return redirect('showTicket')
                
        context = {'form': form}
        return render(request, 'crm/update.html', context)
    else:
        raise PermissionDenied


@login_required(login_url='login')
def deleteTicket(request, ticketID):
    if crmPermission(request.user.username):
        ticket = Ticket.objects.get(TicketID=ticketID)

        if request.method == 'POST':
            ticket.delete()
            return redirect('showTicket')

        context = {'ticket': ticket}
        return render(request, 'crm/delete.html', context)
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
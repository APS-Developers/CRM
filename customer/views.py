from django.shortcuts import redirect, render
from customer.filters import CustomerFilter, OrganisationFilter
from .models import *
from .forms import CreateCustomerForm, CreateOrganisationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.


@login_required(login_url="login")
def createCustomer(request):
    form = CreateCustomerForm()
    if request.method == "POST":
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            customerForm = form.save(commit=False)
            customer = Customer.objects.filter(
                ContactNo=form.cleaned_data.get("ContactNo"),
                Organisation=form.cleaned_data.get("Organisation"),
                Name=form.cleaned_data.get("Name"),
                EmailAddress=form.cleaned_data.get("EmailAddress"),
            )

            if not customer.exists():
                allContactNos = list(Customer.objects.values("ContactNo").distinct())
                for i in range(len(allContactNos)):
                    if (
                        form.cleaned_data.get("ContactNo")
                        == allContactNos[i]["ContactNo"]
                    ):
                        messages.error(
                            request, "Customer with this contact number already exists!"
                        )
                        return redirect("customerDetails")
                customerForm.save()

            return redirect("showCustomer")
    context = {"form": form, "type": "Customer", "name": "Create"}
    return render(request, "customer/create_update.html", context)


@login_required(login_url="login")
def createOrganisation(request):
    form = CreateOrganisationForm()
    if request.method == "POST":
        form = CreateOrganisationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("showOrganisation")
    context = {"form": form, "type": "Organisation", "name": "Create"}
    return render(request, "customer/create_update.html", context)


@login_required(login_url="login")
def showCustomer(request):
    all_customers = Customer.objects.all().order_by("-CustomerID")
    customer_filter = CustomerFilter(request.GET, queryset=all_customers)
    all_customers = customer_filter.qs
    page_number = request.GET.get("page", 1)
    paginator = Paginator(all_customers, 10)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.page_range
    context = {
        "page_obj": page_obj,
        "type": "Customer",
        "customer_filter": customer_filter,
        "page_range": page_range,
    }
    return render(request, "customer/show.html", context)


@login_required(login_url="login")
def showOrganisation(request):
    all_organisations = Organisation.objects.all().order_by("-OrgID")
    organisation_filter = OrganisationFilter(request.GET, queryset=all_organisations)
    all_organisations = organisation_filter.qs
    page_number = request.GET.get("page", 1)
    paginator = Paginator(all_organisations, 10)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.page_range

    context = {
        "page_obj": page_obj,
        "type": "Organisation",
        "organisation_filter": organisation_filter,
        "page_range": page_range,
    }
    return render(request, "customer/show.html", context)


@login_required(login_url="login")
def updateCustomer(request, pk):
    customer = Customer.objects.get(CustomerID=pk)
    form = CreateCustomerForm(instance=customer)

    if request.method == "POST":
        form = CreateCustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            return redirect("showCustomer")

    context = {"form": form, "type": "Customer", "name": "Update"}
    return render(request, "customer/create_update.html", context)


@login_required(login_url="login")
def updateOrganisation(request, pk):
    organisation = Organisation.objects.get(OrgID=pk)
    form = CreateOrganisationForm(instance=organisation)

    if request.method == "POST":
        form = CreateOrganisationForm(request.POST, instance=organisation)

        if form.is_valid():
            organisation = form.save()
            return redirect("showOrganisation")

    context = {"form": form, "type": "Organisation", "name": "Update"}
    return render(request, "customer/create_update.html", context)


@login_required(login_url="login")
def deleteCustomer(request, pk):
    customer = Customer.objects.get(CustomerID=pk)

    if request.method == "POST":
        customer.delete()
        return redirect("showCustomer")

    context = {"customer": customer, "type": "Customer"}
    return render(request, "customer/delete.html", context)


@login_required(login_url="login")
def deleteOrganisation(request, pk):
    organisation = Organisation.objects.get(OrgID=pk)

    if request.method == "POST":
        organisation.delete()
        return redirect("showOrganisation")

    context = {"organisation": organisation, "type": "Organisation"}
    return render(request, "customer/delete.html", context)


def customerDetails(request):
    try:
        name = request.GET.get("name")
        org = request.GET.get("org")
        orgName, orgAddress = org.split(", ")
        customer = Customer.objects.filter(
            Name=name, Organisation__Name=orgName, Organisation__Address=orgAddress
        )
        if not customer:
            return JsonResponse({"error": "No customer found"}, status=404)
        customer = customer.first()
        details = {
            "name": customer.Name,
            "contactNo": str(customer.ContactNo),
            "email": customer.EmailAddress,
            "organisation": customer.Organisation.Name,
            "id": customer.CustomerID,
        }
        return JsonResponse(details)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

from django.shortcuts import render, redirect
from .models import Inventory
from .forms import Form
from .forms import CsvsModelForm
from .filter1 import InventoryFilter
from .models import Csvs
from datetime import datetime
import csv
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from authentication.models import User, UserPermission
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages


def inventoryPermission(username):
    user = User.objects.get(username=username)
    if not user.is_staff or not user.is_superuser:
        permission = UserPermission.objects.get(user_id=user.id).Inventory_permission
    if user.is_staff or user.is_superuser or permission:
        return True
    else:
        return False


@login_required(login_url="login")
def upload_file(request):
    if inventoryPermission(request.user.username):
        form = CsvsModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            form = CsvsModelForm()
            obj = Csvs.objects.filter(activated=False).last()
            with open(obj.file_name.path, "r", encoding="windows-1252") as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if i == 0:
                        pass
                    else:
                        inv = Inventory.objects.create(
                            Make=row[0],
                            Part_Code=row[1],
                            Serial_Number=row[2],
                            Item=row[3],
                            Location=row[4],
                            Purchase_Date=None if not row[5] else row[5],
                            Item_dispatched_Date=None if not row[6] else row[6],
                            Organisation_id=row[7],
                            Status=row[8],
                            CLI_snapshot=row[9],
                            Snapshot_Date=None if not row[10] else row[10],
                        )
                        inv.save()
            obj.activated = True
            obj.save()
            messages.add_message(
                request, messages.SUCCESS, "File uploaded successfully!"
            )
            return redirect("showInventory")
        else:
            for message in form.errors.values():
                messages.add_message(request, messages.ERROR, message)

        return render(request, "inventory/upload.html", {"form": form})
    else:
        raise PermissionDenied


@login_required(login_url="login")
def createInventory(request):
    if inventoryPermission(request.user.username):
        context = {}

        form = Form(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            serialNo = form.cleaned_data.get("Serial_Number")
            messages.add_message(
                request,
                messages.SUCCESS,
                'Product "%s" created successfully!' % serialNo,
            )
            return redirect("showInventory")
        else:
            for message in form.errors.values():
                messages.add_message(request, messages.ERROR, message)

        context["form"] = form
        context["name"] = "Create"
        return render(request, "inventory/create_update.html", context)
    else:
        raise PermissionDenied


@login_required(login_url="login")
def showInventory(request):
    if inventoryPermission(request.user.username):
        all_inventory = Inventory.objects.all().order_by("-Serial_Number")
        Inven_filter = InventoryFilter(request.GET, queryset=all_inventory)
        all_inventory = Inven_filter.qs
        page_number = request.GET.get("page", 1)
        paginator = Paginator(all_inventory, 25)
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        counter = range(page_obj.start_index(), page_obj.end_index() + 1)
        for ctr, item in zip(counter, page_obj.object_list):
            item.counter = ctr
        context = {
            "page_obj": page_obj,
            "inventory_filter": Inven_filter,
            "page_range": page_range,
        }
        return render(request, "inventory/show.html", context)
    else:
        raise PermissionDenied


@login_required(login_url="login")
def updateInventory(request, pk):
    if inventoryPermission(request.user.username):
        inventory = Inventory.objects.get(Serial_Number=pk)
        form = Form(instance=inventory)

        if request.method == "POST":
            form = Form(request.POST, instance=inventory)
            if form.is_valid():
                form.save()
                serialNo = form.cleaned_data.get("Serial_Number")
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Product "%s" updated successfully!' % serialNo,
                )
                return redirect("showInventory")
            else:
                for message in form.errors.values():
                    messages.add_message(request, messages.ERROR, message)

        context = {"form": form, "name": "Update"}
        return render(request, "inventory/create_update.html", context)
    else:
        raise PermissionDenied


def inventoryDetails(request):
    try:
        product = Inventory.objects.get(Serial_Number=request.GET.get("serial"))
        details = {
            "Make": product.Make,
            "PartCode": product.Part_Code,
            "SNo": product.Serial_Number,
            "Item": product.Item,
            "Location": product.Location,
            "Item_dispatched_Date": product.Item_dispatched_Date,
            "Organisation": product.Organisation.__str__(),
            "OrganisationId": product.Organisation.OrgID,
            "Status": product.Status,
        }
        return JsonResponse(details)
    except Exception as e:
        return JsonResponse({"error": "No product found"}, status=404)


def deleteInventory(request, pk):
    item = Inventory.objects.get(Serial_Number=pk)
    if request.method == "POST":
        serialNo = item.Serial_Number
        item.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            'Product "%s" deleted successfully!' % serialNo,
        )
        return redirect("showInventory")

    context = {"item": item}
    return render(request, "inventory/delete.html", context)

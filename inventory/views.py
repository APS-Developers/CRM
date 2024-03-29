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
from django.db import transaction
from django.db.utils import IntegrityError
import re


def inventoryPermission(user):
    if not user.is_staff or not user.is_superuser:
        permission = UserPermission.objects.get(user_id=user.id).Inventory_permission
    if user.is_staff or user.is_superuser or permission:
        return True
    else:
        return False


@login_required(login_url="login")
def upload_file(request):
    if inventoryPermission(request.user):
        form = CsvsModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            form = CsvsModelForm()
            obj = Csvs.objects.filter(activated=False).last()
            if str(obj.file_name).split("/")[1].split(".")[1] != "csv":
                messages.add_message(
                    request,
                    messages.ERROR,
                    "File format not supported! Please upload a CSV file.",
                )
                return redirect("/upload_file")
            try:
                with open(obj.file_name.path, "r", encoding="windows-1252") as f:
                    reader = csv.reader(f)
                    with transaction.atomic():
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
                                    Purchase_Date=datetime.now()
                                    if not row[5]
                                    else row[5],
                                    Item_dispatched_Date=None if not row[6] else row[6],
                                    Organisation_id=row[7],
                                    Status=row[8],
                                    CLI_snapshot=row[9],
                                    Snapshot_Date=None if not row[10] else row[10],
                                )
                                inv.save()
            except IntegrityError as e:
                dup_key = re.search(r"\((?P<key>[a-zA-Z0-9]*)\)", str(e))
                if dup_key:
                    dup_key = dup_key.groupdict().get("key")
                else:
                    dup_key = ""
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"Error while uploading file! Duplicate Serial Number '{dup_key}' found",
                )
                return redirect("/upload_file")
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
    if inventoryPermission(request.user):
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
    if inventoryPermission(request.user):
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
    if inventoryPermission(request.user):
        inventory = Inventory.objects.get(Serial_Number=pk)
        form = Form(instance=inventory)

        if request.method == "POST":
            form = Form(request.POST or None, request.FILES or None, instance=inventory)
            if form.is_valid():
                if "CLI_snapshot" in form.changed_data:
                    inventory.Snapshot_Date = datetime.now()
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

        context = {
            "form": form,
            "name": "Update",
            "CLI_snapshot": inventory.CLI_snapshot,
        }

        return render(request, "inventory/create_update.html", context)
    else:
        raise PermissionDenied


def deleteInventory(request, pk):
    if inventoryPermission(request.user):
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
    else:
        raise PermissionDenied

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404                             
from .models import Inventory
from .forms import Form
from .forms import CsvsModelForm
from .filter1 import InventoryFilter
from .models import Csvs 
from datetime import datetime
import csv
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def upload_file(request):
    form= CsvsModelForm(request.POST or None , request.FILES or None)
    if form.is_valid():
        form.save()
        form=CsvsModelForm()
        obj=Csvs.objects.filter(activated=False).first()
        print(obj.file_name.path)
        with open(obj.file_name.path, 'r',encoding='windows-1252') as f:
            reader=csv.reader(f)
            for i, row in enumerate(reader):
                if i==0:
                    pass
                else:
                    inv = Inventory.objects.create(
                            Make = row[0],
                            Part_Code=row[1],
                            Serial_Number=row[2],
                            Item=row[3],
                            Location=row[4],
                            Purchase_Date=None if not row[5] else row[5],
                            Item_dispatched_Date=None if not row[6] else row[6],
                            Organisation_id=row[7],
                            Status=row[8],
                            Slip=row[9])
                    inv.save()
        obj.activated=True
        obj.save()
    return render(request,'inventory/upload.html',{'form':form})

'''def show_product(request):
    return HttpResponse()'''


@login_required(login_url='login')
def createInventory(request):
    
    context ={}
 
    form = Form(request.POST or None,request.FILES or None)
    print(form.is_valid())
    if form.is_valid():
        form.save()
        return redirect('showInventory')
         
    context['form']= form
    context['name']= 'Create'
    return render(request, "inventory/create_update.html", context)


@login_required(login_url='login')
def showInventory(request):
    all_inventory = Inventory.objects.all()
    Inven_filter = InventoryFilter(request.GET, queryset=all_inventory)
    all_inventory = Inven_filter.qs 
    context = {'inventories': all_inventory, 'inventory_filter': Inven_filter}
    return render(request,'inventory/show.html', context)


@login_required(login_url='login')
def updateInventory(request,pk):
	inventory = Inventory.objects.get(Serial_Number=pk)
	form = Form(instance=inventory)

	if request.method == 'POST':
		form = Form(request.POST, instance=inventory)
		if form.is_valid():
			form.save()
			return redirect('showInventory')

	context = {'form':form, 'name': 'Update'}
	return render(request, 'inventory/create_update.html', context)


# def deleteInventory(request, pk):
# 	inventory = Inventory.objects.get(Serial_Number=pk)
# 	if request.method == "POST":
# 		inventory.delete()
# 		return redirect('/')

# 	context = {'item':inventory}
# 	return render(request, 'create_view.html', context)

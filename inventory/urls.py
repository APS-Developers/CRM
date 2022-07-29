from django.urls import path
from django.contrib import admin
from django_filters.views import FilterView
from . import views

urlpatterns=[
path('createInventory/',views.createInventory, name='createInventory'),
path('upload_file/',views.upload_file),
path('showInventory/',views.showInventory, name='showInventory'),
path('updateInventory/<str:pk>/', views.updateInventory, name='updateInventory'),
path('inventoryDetails/',views.inventoryDetails, name='inventoryDetails'),
# path('deleteInventory/str:pk>/', views.deleteInventory, name='deleteInventory'),
]
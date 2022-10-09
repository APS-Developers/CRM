from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.dashboard, name="reports_dashboard"),
    path("inventory", views.inventory_report, name="inventory_report"),
    path("crm", views.crm_report, name="crm_report"),
]

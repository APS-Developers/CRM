from django.urls import path
from crm import views

urlpatterns = [
    path("customerDetails/", views.customerDetails, name="customerDetails"),
    path(
        "productDetails/<int:customerID>/", views.productDetails, name="productDetails"
    ),
    path("createTicket/", views.createTicket, name="createTicket"),
    path("faultDetails/<int:ticketID>/", views.faultDetails, name="faultDetails"),
    path("updateTicket/<int:ticketID>/", views.updateTicket, name="updateTicket"),
    path("deleteTicket/<int:ticketID>/", views.deleteTicket, name="deleteTicket"),
    path("ticketLog/<int:ticketID>/", views.ticketLog, name="ticketLog"),
    path("showTicket/", views.showTicket, name="showTicket"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("slainfo", views.getTicketSla, name="slainfo"),
    path("slainfomonthly", views.getTicketSlaMonthly, name="slainfomonthly"),
]

from django.urls import path
from crm import views

urlpatterns = [
    path('customerDetails/', views.customerDetails, name='customerDetails'),
    path('productDetails/<int:customerID>/', views.productDetails, name='productDetails'),
    path('faultDetails/<int:ticketID>/', views.faultDetails, name='faultDetails'),
    path('updateTicket/<int:ticketID>/', views.updateTicket, name='updateTicket'),
    path('ticketLog/<int:ticketID>/', views.ticketLog, name='ticketLog'),
    path('showTicket/', views.showTicket, name='showTicket'),
]

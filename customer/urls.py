from django.urls import path
from customer import views

urlpatterns = [
    path('createCustomer/', views.createCustomer, name='createCustomer'),
    path('createOrganisation/', views.createOrganisation, name='createOrganisation'),
    path('showCustomer/', views.showCustomer, name='showCustomer'),
    path('showOrganisation/', views.showOrganisation, name='showOrganisation'),
    path('updateCustomer/<str:pk>/', views.updateCustomer, name='updateCustomer'),
    path('updateOrganisation/<str:pk>/', views.updateOrganisation, name='updateOrganisation'),
    path('deleteCustomer/<str:pk>/', views.deleteCustomer, name='deleteCustomer'),
    path('deleteOrganisation/<str:pk>/', views.deleteOrganisation, name='deleteOrganisation'),
]
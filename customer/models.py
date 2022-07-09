from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

#Create your models here.
class Organisation(models.Model):

    class Meta:
        db_table = "Organisation"

    OrgID = models.AutoField(primary_key=True)
    Name = models.CharField('Name', max_length=100)
    ContactNo = PhoneNumberField('Contact No', unique=True)
    EmailAddress = models.EmailField('Email Address', max_length=200, blank=True)
    Address = models.TextField('Address', max_length=200, unique=True)

    def __str__(self):
        return f"{self.Name}, {self.Address}" 


class Customer(models.Model):

    class Meta:
        db_table = "Customer"

    CustomerID = models.AutoField(primary_key=True)
    Name = models.CharField('Name', max_length=100)
    ContactNo = PhoneNumberField('Contact No')
    EmailAddress = models.EmailField('Email Address', max_length=200, blank=True)
    Organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


    # customer hoga foreign key
    # Organisation = models.CharField(max_length=100)     # drop down , auto-populate also editable
    # CustomerName = models.CharField('Customer Name', max_length=100)
    # ContactNo = PhoneNumberField('Contact No')
    # EmailAddress = models.EmailField('Email Address', max_length=200, blank=True)

# organisation table -> name, pta, id, email, location, contact, 
# customer table -> id, CustomerName, ContactNo, EmailAddress, org id by the name of org - foreign key

# django, get create
# reverse lookup - one to many 

# nupur ko dena hai id aur naam
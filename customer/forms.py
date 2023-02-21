from django.forms import ModelForm
from .models import Customer, Organisation
from django import forms
from phonenumber_field.formfields import PhoneNumberField


class CreateCustomerForm(ModelForm):
    Name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingInput",
                "type": "name",
                "placeholder": "Name",
            }
        ),
        label="",
    )

    Organisation = forms.ModelChoiceField(
        queryset=Organisation.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select mb-3 form-select-md mb-3",
                "aria-label": ".form-select-md example",
                "type": "organisation",
                "placeholder": "Organisation",
            }
        ),
        label="",
    )

    ContactNo = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "id": "floatingInput",
                "placeholder": "ContactNo",
            }
        ),
        label="",
    )

    EmailAddress = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-input",
                "type": "email",
                "id": "floatingInput",
                "placeholder": "EmailAddress",
            }
        ),
        label="",
    )

    class Meta:
        model = Customer
        fields = ["Name", "Organisation", "ContactNo", "EmailAddress"]


class CreateOrganisationForm(ModelForm):
    Name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingInput",
                "type": "name",
                "placeholder": "ContactNo",
            }
        ),
        label="",
    )

    ContactNo = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-input",
                "type": "number",
                "id": "floatingInput",
                "placeholder": "Phone",
            }
        ),
        label="",
    )

    EmailAddress = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "type": "email",
                "id": "floatingInput",
                "placeholder": "EmEmailAddressail",
            }
        ),
        label="",
    )

    Address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "type": "address",
                "id": "floatingTextarea",
                "placeholder": "Address",
                "style": "height: 100px",
            }
        ),
        label="",
    )

    class Meta:
        model = Organisation
        fields = ["Name", "ContactNo", "EmailAddress", "Address"]

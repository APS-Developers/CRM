from django.forms import ModelForm
from inventory.models import Inventory
from .models import Ticket
from customer.models import Customer, Organisation
from django import forms
from phonenumber_field.formfields import PhoneNumberField

boolChoices = [(True, "Yes"), (False, "No")]

priorityChoices = [("P1", "P1"), ("P2", "P2"), ("P3", "P3"), ("P4", "P4")]

faultChoices = [
    ("Router", "Router faulty"),
    ("Modem", "Modem faulty"),
    ("Switch", "Switch faulty"),
]

resolutionChoices = [("123", "Router faulty"), ("456", "Modem faulty")]

statusChoices = [
    ("Open", "Open"),
    ("Resolved", "Resolved"),
    ("Pending", "Pending"),
    ("Closed", "Closed"),
]


class CustomerForm(ModelForm):

    Name = forms.CharField(
        widget=forms.TextInput(attrs={"id": "", "type": "text"}), label=""
    )

    Organisation = forms.ModelChoiceField(
        queryset=Organisation.objects.all(),
        widget=forms.Select(attrs={"id": ""}),
        label="",
    )

    ContactNo = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "phone",
                "id": "",
            }
        ),
        label="",
    )

    EmailAddress = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "type": "email",
                "id": "",
            }
        ),
        label="",
    )

    class Meta:
        model = Customer
        fields = ["Name", "Organisation", "ContactNo", "EmailAddress"]


class ProductForm(ModelForm):
    class Meta:
        model = Ticket
        fields = []


class FaultForm(ModelForm):

    SerialNo = forms.CharField(
        widget=forms.TextInput(attrs={"id": "", "type": "text"}), label=""
    )

    Category = forms.CharField(
        widget=forms.TextInput(attrs={"id": "", "type": "text"}), label=""
    )

    SubCategory = forms.CharField(
        widget=forms.TextInput(attrs={"id": "", "type": "text"}), label=""
    )

    Priority = forms.ChoiceField(
        choices=priorityChoices, widget=forms.Select(attrs={"id": ""}), label=""
    )

    FaultFoundCode = forms.ChoiceField(
        choices=faultChoices, widget=forms.Select(attrs={"id": ""}), label=""
    )

    Summary = forms.CharField(
        widget=forms.Textarea(
            attrs={"id": "", "type": "text", "cols": "30", "rows": "5"}
        ),
        label="",
    )

    class Meta:
        model = Ticket
        fields = [
            "SerialNo",
            "Category",
            "SubCategory",
            "Priority",
            "FaultFoundCode",
            "Summary",
        ]


class UpdateForm(ModelForm):

    TicketID = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "readonly"}), label=""
    )

    DateCreated = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "readonly"}), label=""
    )

    Status = forms.ChoiceField(
        choices=statusChoices, widget=forms.Select(attrs={"id": ""}), label=""
    )

    SerialNo = forms.CharField(
        widget=forms.TextInput(
            attrs={"readonly": "readonly", "id": "", "type": "text"}
        ),
        label="",
    )

    # ModelNo = forms.CharField(
    #     widget=forms.TextInput(attrs={"id": "", "type": "text"}), label=""
    # )

    Category = forms.CharField(
        widget=forms.TextInput(attrs={"id": "", "type": "text"}), label=""
    )

    SubCategory = forms.CharField(
        widget=forms.TextInput(attrs={"id": "", "type": "text"}), label=""
    )

    Priority = forms.ChoiceField(
        choices=priorityChoices, widget=forms.Select(attrs={"id": ""}), label=""
    )

    FaultFoundCode = forms.ChoiceField(
        choices=faultChoices, widget=forms.Select(attrs={"id": ""}), label=""
    )

    ResolutionCode = forms.ChoiceField(
        choices=resolutionChoices, widget=forms.Select(attrs={"id": ""}), label=""
    )

    OnlineResolvable = forms.ChoiceField(
        choices=boolChoices, widget=forms.Select(attrs={"id": ""}), label=""
    )

    ResolutionRemarks = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"id": "", "type": "text", "cols": "30", "rows": "5"}
        ),
        label="",
    )

    AlternateHW = forms.ModelChoiceField(
        required=False,
        queryset=Inventory.objects.filter(Organisation=None),
        widget=forms.Select(attrs={"id": ""}),
        label="",
    )

    Summary = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"id": "", "type": "text", "cols": "30", "rows": "5"}
        ),
        label="",
    )

    DateClosed = forms.DateField(
        required=False, widget=forms.TextInput(attrs={"readonly": "readonly"}), label=""
    )

    class Meta:
        model = Ticket
        fields = [
            "DateCreated",
            "TicketID",
            "Status",
            "Category",
            "SubCategory",
            "SerialNo",
            "Summary",
            "Priority",
            "FaultFoundCode",
            "ResolutionCode",
            "ResolutionRemarks",
            "OnlineResolvable",
            "AlternateHW",
            "DateClosed",
        ]

from django.forms import ModelForm
from inventory.models import Inventory
from .models import Ticket
from customer.models import Customer, Organisation
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.db.models import Q

boolChoices = [("", "---------"), ("Yes", "Yes"), ("No", "No")]

priorityChoices = [("P1", "P1"), ("P2", "P2"), ("P3", "P3"), ("P4", "P4")]

statusChoices = [
    ("Open", "Open"),
    ("Pending", "Pending"),
    ("Resolved", "Resolved"),
    ("Closed", "Closed"),
]

faultFoundChoices = [
    ("", "---------"),
    ("Power Issue", "Power Issue"),
    ("External Card Faulty", "External Card Faulty"),
    ("Router DRM Issue", "Router DRM Issue"),
    ("Port Faulty", "Port Faulty"),
    ("FAN not working", "FAN not working"),
    ("Power Supply Faulty", "Power Supply Faulty"),
    ("Not Booting", "Not Booting"),
    ("Unable to take Console", "Unable to take Console"),
    ("Line Card Faulty", "Line Card Faulty"),
    ("SUP Card Faulty", "SUP Card Faulty"),
    ("Physical Damage", "Physical Damage"),
    ("Others", "Others"),
    ("Hardware not in AMC", "Hardware not in AMC"),
]

resolutionChoices = [
    ("", "---------"),
    ("Power Issue Resolved with Hard Reset", "Power Issue Resolved with Hard Reset"),
    ("External Card Dispatched", "External Card Dispatched"),
    ("DRM Issue Resolved", "DRM Issue Resolved"),
    ("New Hardware Dispatched", "New Hardware Dispatched"),
    ("FAN/Module Dispatched", "FAN/Module Dispatched"),
    ("Power Supply Replaced/Dispatched", "Power Supply Replaced/Dispatched"),
    ("Booting Issue Resolved", "Booting Issue Resolved"),
    ("Console Issues Resolved", "Console Issues Resolved"),
    ("Line Card Replaced/Dispatched", "Line Card Replaced/Dispatched"),
    ("SUP Card Replaced/Dispatched", "SUP Card Replaced/Dispatched"),
    ("Physical Damage - Not covered in AMC", "Physical Damage - Not covered in AMC"),
    ("Others", "Others"),
]

dispatchedChoices = [
    ("", "---------"),
    ("DTDC", "DTDC"),
    ("BLUEDART", "BLUEDART"),
    ("MARUTI", "MARUTI"),
    ("DELHIVERY", "DELHIVERY"),
    ("SAFEXPRESS", "SAFEXPRESS"),
    ("GATI", "GATI"),
]

deliveryStatus = [
    ("", "---------"),
    ("Dispatched", "Dispatched"),
    ("In Transit", "In Transit"),
    ("Out for Delivery", "Out for Delivery"),
    ("Delivered", "Delivered"),
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
    SerialNo = forms.ModelChoiceField(
        queryset=Inventory.objects.filter(~Q(Organisation=None)),
        widget=forms.Select(attrs={"id": "", "type": "text"}),
        label="",
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

    # FaultFoundCode = forms.CharField(widget=forms.TextInput(attrs={"id": ""}), label="")

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

    # SerialNo = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={"readonly": "readonly", "id": "", "type": "text"}
    #     ),
    #     label="",
    # )
    SerialNo = forms.ModelChoiceField(
        queryset=Inventory.objects.filter(~Q(Organisation=None)),
        widget=forms.TextInput(
            attrs={"readonly": "readonly", "id": "", "type": "text"}
        ),
        label="",
    )

    # ModelNo = forms.CharField(
    #     widget=forms.TextInput(attrs={"id": "", "type": "text"}), label=""
    # )

    Category = forms.CharField(
        widget=forms.TextInput(
            attrs={"readonly": "readonly", "id": "", "type": "text"}
        ),
        label="",
    )

    SubCategory = forms.CharField(
        widget=forms.TextInput(
            attrs={"readonly": "readonly", "id": "", "type": "text"}
        ),
        label="",
    )

    # Priority = forms.ChoiceField(
    #     choices=priorityChoices, widget=forms.Select(attrs={"readonly": "readonly","id": ""}), label=""
    # )
    Priority = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "readonly", "id": ""}), label=""
    )

    # FaultFoundCode = forms.CharField(
    #     widget=forms.TextInput(attrs={"id": ""}), label=""
    # )

    FaultFoundCode = forms.ChoiceField(
        required=False,
        choices=faultFoundChoices,
        widget=forms.Select(attrs={"id": ""}),
        label="",
    )

    ResolutionCode = forms.ChoiceField(
        required=False,
        choices=resolutionChoices,
        widget=forms.Select(attrs={"id": ""}),
        label="",
    )

    OnlineResolvable = forms.ChoiceField(
        required=False,
        choices=boolChoices,
        widget=forms.Select(attrs={"id": ""}),
        label="",
    )

    ResolutionRemarks = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"id": "", "type": "text", "cols": "30", "rows": "5"}
        ),
        label="",
    )

    HWDispatched = forms.ModelChoiceField(
        required=False,
        queryset=Inventory.objects.all(),
        widget=forms.Select(attrs={"id": "HWDispatched", "class": "d-none"}),
        label="",
    )
    HWDispatchedSerial = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "HWDispatchedSerial",
                "type": "text",
                "list": "HWDispatchedSerialList",
            }
        ),
        label="Hardware Dispatched",
    )

    Summary = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "readonly": "readonly",
                "id": "",
                "type": "text",
                "cols": "30",
                "rows": "5",
            }
        ),
        label="",
    )

    Notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"id": "", "type": "text", "cols": "30", "rows": "5"}
        ),
        label="",
    )

    ResolutionDate = forms.DateField(
        required=False, widget=forms.TextInput(attrs={"readonly": "readonly"}), label=""
    )

    DocketNumber = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"id": "", "type": "text", "cols": "30", "rows": "1"}
        ),
        label="",
    )

    DispatchedThrough = forms.ChoiceField(
        required=False,
        choices=dispatchedChoices,
        widget=forms.Select(attrs={"id": ""}),
        label="",
    )

    DeliveryStatus = forms.ChoiceField(
        required=False,
        choices=deliveryStatus,
        widget=forms.Select(attrs={"id": ""}),
        label="",
    )

    Notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"id": "", "type": "text", "cols": "30", "rows": "2"}
        ),
        label="",
    )
    ClosureDate = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={"id": "", "type": "date"}),
        label="",
    )
    ClosureRemarks = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"id": "", "type": "text", "cols": "30", "rows": "2"}
        ),
        label="",
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
            "HWDispatched",
            "ResolutionDate",
            "DocketNumber",
            "DispatchedThrough",
            "DeliveryStatus",
            "Notes",
            "ClosureDate",
            "ClosureRemarks",
        ]

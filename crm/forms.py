from django.forms import ModelForm
from inventory.models import Inventory
from .models import Ticket
from customer.models import Customer, Organisation
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.db.models import Q


class CustomerForm(ModelForm):
    Name = forms.CharField(
        widget=forms.TextInput(attrs={"id": "aps_crm_customer_name", "type": "text"}),
        label="",
    )

    ContactNo = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "phone",
                "id": "aps_crm_customer_phone",
            }
        ),
        label="",
    )

    EmailAddress = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "type": "email",
                "id": "aps_crm_customer_email",
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


class CreateTicketForm(ModelForm):
    SerialNo = forms.ModelChoiceField(
        queryset=Inventory.objects.filter(~Q(Organisation=None)),
        widget=forms.Select(attrs={"id": "", "type": "text"}),
        label="",
    )

    Category = forms.ChoiceField(
        choices=Ticket.categoryChoices, widget=forms.Select(attrs={"id": ""}), label=""
    )

    SubCategory = forms.ChoiceField(
        choices=Ticket.subCategoryChoices,
        widget=forms.Select(attrs={"id": ""}),
        label="",
    )

    Priority = forms.ChoiceField(
        choices=Ticket.priorityChoices, widget=forms.Select(attrs={"id": ""}), label=""
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
        choices=Ticket.statusChoices, widget=forms.Select(attrs={"id": ""}), label=""
    )

    SerialNo = forms.ModelChoiceField(
        queryset=Inventory.objects.filter(~Q(Organisation=None)),
        widget=forms.TextInput(
            attrs={"readonly": "readonly", "id": "", "type": "text"}
        ),
        label="",
    )

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

    Priority = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "readonly", "id": ""}), label=""
    )

    FaultFoundCode = forms.ChoiceField(
        required=False,
        choices=Ticket.faultFoundChoices,
        widget=forms.Select(attrs={"id": ""}),
        label="",
    )

    ResolutionCode = forms.ChoiceField(
        required=False,
        choices=Ticket.resolutionChoices,
        widget=forms.Select(attrs={"id": ""}),
        label="",
    )

    OnlineResolvable = forms.ChoiceField(
        required=False,
        choices=Ticket.boolChoices,
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
        queryset=None,
        widget=forms.TextInput(
            attrs={
                "id": "HWDispatched",
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
        choices=Ticket.dispatchedChoices,
        widget=forms.Select(attrs={"id": ""}),
        label="",
    )

    DeliveryStatus = forms.ChoiceField(
        required=False,
        choices=Ticket.deliveryStatus,
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.HWDispatched:
            self.fields["HWDispatched"].queryset = Inventory.objects.filter(
                Q(Organisation=None)
                | Q(Serial_Number=self.instance.HWDispatched.Serial_Number)
            )
        else:
            self.fields["HWDispatched"].queryset = Inventory.objects.filter(
                Organisation=None
            )
        if self.instance.Status == "Resolved":
            print("Resolved")
            for field in self.fields:
                if field not in ["Status", "Notes"]:
                    self.fields[field].widget.attrs["readonly"] = "readonly"
            self.fields["Status"].choices = [
                ("Resolved", "Resolved"),
                ("Open", "Reopen"),
            ]

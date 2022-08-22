from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from authentication.models import UserPermission
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm



class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-input',
        'id': 'floatingInput',
        'type': 'username',
        'placeholder': 'Username'
    }), label='')

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-input',
        'id': 'floatingInput',
        'type': '',
        'placeholder': 'Email'
        }), label='')

    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-input',
        'type': 'password',
        'id': 'floatingPassword',
        'placeholder': 'Password'
        }), label='')

    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-input',
        'type': 'password',
        'id': 'floatingPassword',
        'placeholder': 'Password'
        }), label='')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserPermissionsForm(forms.ModelForm):
    CRM_permission = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'id': 'flexSwitchCheckDefault',
        'type': 'checkbox',
        'placeholder': 'CRM Permission'
    }), label='')

    Inventory_permission = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'id': 'flexSwitchCheckDefault',
        'type': 'checkbox',
        'placeholder': 'Inventory Permission'
    }), label='')

    class Meta:
        model = UserPermission
        fields = ['CRM_permission', 'Inventory_permission']


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(attrs={
        'class': 'form-control aps_login_form',
        'id': 'floatingInput',
        'type': 'username',
        'placeholder': 'username',
    }), label='')
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control aps_login_form',
            'placeholder': 'password',
            'id': 'floatingPassword',
            'type': 'password'
        }
    ))


class UserPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'type': 'email',
        'id': 'floatingInput'
        }))


class UserPasswordChangeForm(SetPasswordForm):

    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-input',
        'type': 'password',
        'id': 'floatingPassword',
        }), label='')

    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-input',
        'type': 'password',
        'id': 'floatingPassword',
        }), label='')
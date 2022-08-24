from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from authentication.forms import CreateUserForm, UserPermissionsForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from authentication.models import UserPermission
from .filters import UserFilter

# Create your views here.


def index(request):
    return render(request, "home/index.html")


@login_required(login_url="login")
def createUser(request):
    form = CreateUserForm()
    permissions_form = UserPermissionsForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        permissions_form = UserPermissionsForm(request.POST)

        if form.is_valid() and permissions_form.is_valid():
            user = form.save()
            permissions = permissions_form.save(commit=False)
            permissions.user = user
            permissions.save()

            # username = form.cleaned_data.get('username')
            # if username == User.objects.get(username=username).username:
            #     messages.error(request, "Username already exists!")
            #     return redirect('create')

            # messages.success(request, 'Account was created successfully for ' + username)
            return redirect("showUser")

    context = {"form": form, "permissions_form": permissions_form, "name": "Create"}
    return render(request, "authentication/create_update.html", context)


def loginUser(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        form = UserLoginForm()

        if request.method == "POST":
            form = UserLoginForm(request, data=request.POST)

            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect("dashboard")
                else:
                    messages.info(request, "Username or Password is incorrect")

        context = {"form": form}
        return render(request, "authentication/login.html", context)


@never_cache
@login_required(login_url="login")
def dashboard(request):
    return render(request, "dashboardNavbar.html")


@login_required(login_url="login")
def showUser(request):
    all_users = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=all_users)
    all_users = user_filter.qs
    context = {"all_users": all_users, "user_filter": user_filter}
    return render(request, "authentication/show.html", context)


def logoutUser(request):
    logout(request)
    return redirect("index")


@login_required(login_url="login")
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    form = CreateUserForm(instance=user)

    user_permissions = UserPermission.objects.get(user_id=pk)
    permissions_form = UserPermissionsForm(instance=user_permissions)

    if request.method == "POST":
        form = CreateUserForm(request.POST, instance=user)
        permissions_form = UserPermissionsForm(request.POST, instance=user_permissions)

        if form.is_valid() and permissions_form.is_valid():
            user = form.save()
            permissions = permissions_form.save(commit=False)
            permissions.user_id = user.id
            permissions.save()
            return redirect("showUser")

    context = {"form": form, "permissions_form": permissions_form, "name": "Update"}
    return render(request, "authentication/create_update.html", context)


@login_required(login_url="login")
def deleteUser(request, pk):
    user = User.objects.get(id=pk)

    if request.method == "POST":
        user.delete()
        return redirect("showUser")

    context = {"user": user}
    return render(request, "authentication/delete.html", context)

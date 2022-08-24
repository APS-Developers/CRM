from django.urls import path
from authentication import views
from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm, UserPasswordChangeForm

# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.createUser, name="create"),
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("update/<str:pk>/", views.updateUser, name="update"),
    path("delete/<str:pk>/", views.deleteUser, name="delete"),
    path("showUser/", views.showUser, name="showUser"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="authentication/password_reset.html",
            form_class=UserPasswordResetForm,
        ),
        name="password_reset",
    ),  # submit email form
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="authentication/password_reset_done.html",
        ),
        name="password_reset_done",
    ),  # email sent success message
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="authentication/password_reset_confirm.html",
            form_class=UserPasswordChangeForm,
        ),
        name="password_reset_confirm",
    ),  # link to password reset form in mail
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="authentication/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),  # password successfully changed message
]

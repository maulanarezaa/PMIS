from django.urls import path
from . import viewsLogin

urlpatterns = [
    path("login", viewsLogin.loginview, name="login"),
    path("logout", viewsLogin.logout_view, name="logout"),
]

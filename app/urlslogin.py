from django.urls import path
from . import viewsLogin
from . import viewsService

urlpatterns = [
    path("login", viewsLogin.loginview, name="login"),
    path("logout", viewsLogin.logout_view, name="logout"),
    path(
        "users",
        viewsService.user_list,
        name="user_list"
    ),

    path(
        "users/create/",
        viewsService.user_create,
        name="user_create"
    ),
    path(
        "users/<int:user_id>/job-order/",
            viewsService.assign_job_order,
        name="assign_job_order"
    ),

]

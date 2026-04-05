from django.urls import path
from . import viewsDashboard


urlpatterns = [
    path("", viewsDashboard.viewdashboard, name="dashboard"),
]

from django.urls import path
from . import viewsProject


urlpatterns = [
    path("viewjoborder", viewsProject.viewjoborder, name="viewjoborder"),
    path("joborder/add", viewsProject.tambahdatajoborder, name="tambahdatajoborder"),
    path(
        "joborder/detail/<str:id>",
        viewsProject.viewdetailjoborder,
        name="detailjoborder",
    ),
    path("workcompletion", viewsProject.viewworkcompletion, name="viewworkcompletion"),
    path(
        "workcompletion/add",
        viewsProject.tambahdataworkcompletion,
        name="tambahdataworkcompletion",
    ),
    path("search-jo/", viewsProject.search_jo, name="search_jo"),
]

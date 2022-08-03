from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("random", views.randompage, name="randompage"),
    path("createpage", views.createpage, name = "createpage"),  
    path("<str:name>",views.entry, name = "entry"),
    path("<str:name>/edit",views.edit,name="edit" ),
    
    
]

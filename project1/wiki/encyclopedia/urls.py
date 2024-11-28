from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:input>/", views.entry, name="entries"),
    path("search/", views.search_result, name="search_result"),
    path("random/", views.random_page, name="random"),
    path("create/", views.new_page, name="new"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit")
]

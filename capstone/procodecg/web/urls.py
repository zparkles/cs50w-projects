from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("calendar", views.calendar, name="calendar"),
    path("progress", views.progress, name="progress"),
    path("programs", views.programs, name="programs"),

    #API ROUTES
    path("events", views.events, name="events"),
    path("schedule", views.schedule, name="schedule"),
    path("cards", views.newCard, name="newCard"),
    path("cards/<int:card_id>", views.card, name="card"),
    path("students/<int:student_id>", views.personalCards, name="personalCards")
]

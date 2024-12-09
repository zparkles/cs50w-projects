from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing_page, name="listing"),
    path("category/<str:input>", views.cat_page, name="category page"),
    path("<int:listing_id>/close", views.close, name = "close"),
    path("addwatchlist/<int:listing_id>", views.watchlist, name = "watchlist"),
    path("removewatchlist/<int:listing_id>", views.remove_watchlist, name = "delete watchlist"),
    path("watchlist/<int:user_id>", views.watchlist_page, name="watchlist_page"),
    
]

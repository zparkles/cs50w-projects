
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following_page, name="following-page"),
    


    #API URLS
    path('profile/follow', views.following, name="follow"),
    path("<int:post_id>/edit", views.edit, name= "edit"),
    path('profile/follow/<int:follow_id>', views.unfollowing, name="unfollow"),
    path('like', views.liking, name="like"),
    path('like/<int:like_id>', views.unliking, name="unlike"),
    path("allposts", views.all_posts, name="all"),
    path("count/<int:post_id>", views.count_like, name = "count"),
]

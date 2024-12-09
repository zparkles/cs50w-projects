from django.contrib import admin

from .models import Listings, User, Bid, Comment, Watchlist
# Register your models here.

admin.site.register(Listings)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
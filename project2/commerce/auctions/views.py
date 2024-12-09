from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from .models import User, Listings, Bid, Comment, Watchlist



def index(request):
    #if not request.user.is_authenticated:
     #   return HttpResponseRedirect(reverse("login"))
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create (request):
    if request.method == "POST":
       title = request.POST["title"]
       description = request.POST["description"]
       current_bid = request.POST["current_bid"]
       image = request.FILES['image']
       category = request.POST["category"]
       author = request.user
       
       try: 
            post = Listings.objects.create_listing(title, description, current_bid, image,category, author)
            post.save()
       except:
           return render(request, "auctions/create.html", {
                "message": "Cannot create post."
            })
       return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html")
       

def listing_page (request, listing_id):
    post = Listings.objects.get(pk=listing_id)
    bid_exist = Bid.objects.filter(bid_object = listing_id)
    try:
        watchlist = Watchlist.objects.get(item=listing_id)
    except Watchlist.DoesNotExist:
        watchlist = None
    if bid_exist:
        top_bid = Bid.objects.filter(bid_object = listing_id).latest('bid')
        if request.method == "POST":
            bid = request.POST["bid"]
            bidder = request.user
            comment = request.POST["comment"]
            
            if not comment.strip():  
                if Decimal(bid) <= top_bid.bid:
                    return render(request, "auctions/listing.html", {
                    "message": "The bid should be greater than the current value.",
                    "listing": post,
                    "comments": Comment.objects.filter(comment_object = listing_id),
                    "top_bid": top_bid,
                    "watchlist": watchlist
                })
                elif Decimal(bid) >= post.current_bid :
                    post.current_bid = Decimal(bid)
                    bid_made = Bid.objects.create_bid(bid, bidder, post)
                    post.save()
                    bid_made.save()
                    return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        
            elif not bid.strip():
                comment_made = Comment.objects.create_comment(comment, bidder, post)
                comment_made.save()
                return HttpResponseRedirect(reverse("listing", args=[listing_id]))
            else:
                if Decimal(bid) <= top_bid.bid:
                    comment_made = Comment.objects.create_comment(comment, bidder, post)
                    comment_made.save()
                    return render(request, "auctions/listing.html", {
                    "message": "The bid should be greater than the current value.",
                    "listing": post,
                    "comments": Comment.objects.filter(comment_object = listing_id),
                    "top_bid": top_bid,
                    "watchlist": watchlist
                })
                elif Decimal(bid) >= post.current_bid :
                    post.current_bid = Decimal(bid)
                    bid_made = Bid.objects.create_bid(bid, bidder, post)
                    post.save()
                    bid_made.save()
                    comment_made = Comment.objects.create_comment(comment, bidder, post)
                    comment_made.save()
                    return HttpResponseRedirect(reverse("listing"), args=[listing_id])
        return render(request, "auctions/listing.html", {
            "listing": post,
            "comments": Comment.objects.filter(comment_object = listing_id),
            "top_bid" : top_bid,
            "bid_exist" : bid_exist,
            "watchlist": watchlist
        }) 

    else:
        if request.method == "POST":
            bid = request.POST["bid"]
            bidder = request.user
            comment = request.POST["comment"]
            if not comment.strip():  
                if Decimal(bid) >= post.current_bid :
                    post.current_bid = Decimal(bid)
                    bid_made = Bid.objects.create_bid(bid, bidder, post)
                    post.save()
                    bid_made.save()
                    return HttpResponseRedirect(reverse("listing", args=[listing_id]))
                else:
                    return render(request, "auctions/listing.html", {
                    "message": "The bid should at least have the same value as the starting bid.",
                    "listing": post,
                    "comments": Comment.objects.filter(comment_object = listing_id),
                    "watchlist": watchlist
                }) 
            elif not bid.strip():
                comment_made = Comment.objects.create_comment(comment, bidder, post)
                comment_made.save()
                return HttpResponseRedirect(reverse("listing", args=[listing_id]))
            else:
                if Decimal(bid) >= post.current_bid :
                    post.current_bid = Decimal(bid)
                    post.save()
                    bid_made = Bid.objects.create_bid(bid, bidder, post)
                    bid_made.save()
                    comment_made = Comment.objects.create_comment(comment, bidder, post)
                    comment_made.save()
                    return HttpResponseRedirect(reverse("listing", args=[listing_id]))
                else:
                    comment_made = Comment.objects.create_comment(comment, bidder, post)
                    comment_made.save()
                    return render(request, "auctions/listing.html", {
                    "message": "The bid should at least have the same value as the starting bid.",
                    "listing": post,
                    "comments": Comment.objects.filter(comment_object = listing_id),
                    "watchlist": watchlist
                })
            

    return render(request, "auctions/listing.html", {
        "listing": post,
        "comments": Comment.objects.filter(comment_object = listing_id),
        "watchlist": watchlist

    }) 

def cat_page(request, input):
    return render(request, "auctions/category.html", {
        "category": Listings.objects.filter(category = str(input)),
        "input" : input

    }) 

@login_required
def watchlist_page(request, user_id):
    watchlist = Watchlist.objects.filter(user = user_id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    } )

def watchlist(request, listing_id):
    post = Listings.objects.get(pk=listing_id)
    item_added = Watchlist.objects.add_watchlist(request.user, post)
    item_added.save()
    return HttpResponseRedirect(reverse("watchlist_page", args=[request.user.id]))

def remove_watchlist(request, listing_id):
    post = Listings.objects.get(pk=listing_id)
    item = Watchlist.objects.filter(user = request.user, item = post)
    item.delete()
    return HttpResponseRedirect(reverse("watchlist_page", args=[request.user.id]))

def close(request, listing_id):
    post = Listings.objects.get(pk=listing_id)
    bid = Bid.objects.filter(bid_object = listing_id).latest('bid')
    post.status = False
    bid.winner = True
    post.save()
    bid.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))
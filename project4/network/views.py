import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.order_by("-date_posted").all()
    paginator = Paginator(posts,2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
       post = request.POST["post"]     
       author = request.user
       
       try: 
            create = Post.objects.create_post(post, author)
            create.save()
       except:
           return render(request, "network/index.html", {
                "message": "Cannot create post."
            })
       return HttpResponseRedirect(reverse("index"))
    return render(request, "network/index.html", {
        'page_obj': page_obj,
    })

def profile(request,user_id):
    #user = request.user
    posts = Post.objects.filter(author=user_id).order_by("-date_posted").all()
    follower_count = Follow.objects.filter(account=user_id, follow=True).count()
    following_count = Follow.objects.filter(user=user_id, follow=True).count()
    if request.user.id == user_id :
        follow_status = None
    else:
        try:
            follow_status = Follow.objects.get(account=user_id, user= request.user)
        except: 
            follow_status = None

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "author": User.objects.get(pk=user_id),
        "follow_status" : follow_status,
        "follower_count": follower_count,
        "following_count" : following_count,
        'page_obj': page_obj})

def all_posts(request):
    posts = Post.objects.order_by("-date_posted").all()
    if request.method == 'GET':
         return JsonResponse([post.serialize() for post in posts], safe=False)
        


@login_required
def following_page(request):
    MyFollowing = Follow.objects.filter(user=request.user.id, follow=True)
    following_post = []
    for i in MyFollowing:
        post = Post.objects.get(author = i.account.id)
        following_post.append(post)
        following_post.sort(key=lambda post: post.date_posted, reverse=True)
    paginator = Paginator(following_post, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'network/following_page.html', {
        'page_obj': page_obj,
        
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def edit (request, post_id):
    post_query = Post.objects.get(pk=post_id)
    if request.method == "GET":
        return JsonResponse(post_query.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("post") is not None:
            post_query.post = data["post"]
        
        post_query.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
   

@login_required
def following(request):

    if request.method == "POST":

        data = json.loads(request.body)

        follow = data.get("follow", "")
        account = User.objects.get(pk= data.get("account", ""))

        
        follow_status = Follow(
                account= account,
                user=request.user,
                follow = follow
            )
        follow_status.save()

        return JsonResponse({"message": "You're following this account!"}, status=201) 

    elif request.method == 'GET':
         follow_query = Follow.objects.all()
         if request.method == 'GET':
            return JsonResponse([follow.serialize() for follow in follow_query], safe=False)
        

    
@login_required
def refollowing (request, follow_id):
    follow_data = Follow.objects.get(pk=follow_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("follow") is not None:
            follow_data.follow = data["follow"]
        
        follow_data.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400) 



@login_required
def unfollowing (request, follow_id):
    follow_data = Follow.objects.get(pk=follow_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("follow") is not None:
            follow_data.follow = data["follow"]
        
        follow_data.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400) 
    

@login_required
def liking(request):

    if request.method == "POST":

        data = json.loads(request.body)

        status = data.get("status", "")
        post_liked = Post.objects.get(pk= data.get("post_liked", ""))

        like_status = Like(
                user=request.user,
                status = status,
                post_liked = post_liked

            )
        like_status.save()

        return JsonResponse({"message": "You liked this post!"}, status=201) 

    elif request.method == 'GET':
        try:
            like_query = Like.objects.all()  # Fetch all likes
            likes = [like.serialize() for like in like_query]
            return JsonResponse(likes, safe=False)
        except Like.DoesNotExist:
            return JsonResponse({"error": "Data not found."}, status=404)


        

    
@login_required
def return_like (request, like_id):
    like_data = Like.objects.get(pk=like_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("status") is not None:
            like_data.status = data["status"]
        
        like_data.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400) 



@login_required
def unliking (request, like_id):
    like_data = Like.objects.get(pk=like_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("status") is not None:
            like_data.status = data["status"]
        
        like_data.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400) 

def count_like(request, post_id):
    post = Post.objects.get(pk = post_id)
    like_data = Like.objects.filter(post_liked = post_id, status = True).count()
    if request.method == "GET":
       
        post.like_count = like_data
        
        post.save()
        return JsonResponse(post.serialize())


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
import json
import os
from django.core.paginator import Paginator



current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'static', 'programs.json')


# Create your views here.

def index(request) :
    return render (request, 'web/index.html')


def calendar(request) :
    return render (request, 'web/calendar.html')


def events(request):
    if request.method == 'GET':
        try:
            event_query = Event.objects.filter(
            students= None
        ) 
            events = [e.serialize() for e in event_query]
            return JsonResponse(events, safe=False)
        except Event.DoesNotExist:
            return JsonResponse({"error": "Data not found."}, status=404)
        
@login_required
def schedule(request) :
   
    events = Event.objects.filter(
            students=request.user
        )

    return JsonResponse([event.serialize() for event in events], safe=False)
        

# REGISTER & LOGIN 
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user.verification == True:
            if user is not None :
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "web/login.html", {
                    "message": "Invalid username and/or password."
                })
        else:
                return render(request, "web/login.html", {
                    "message": "Account hasn't been verified."
                })
    else:
        return render(request, "web/login.html")


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
            return render(request, "web/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "web/register.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "web/register.html")

#PROGRAMS

def programs (request):
    programs_data = open(file_path)
    data = json.load(programs_data) 
    return render (request, 'web/programs.html', {
        "data": data
    })



#STUDENTS' CARDS
def progress (request):
    students = User.objects.exclude(username = 'zparkles').filter(verification = True)
    cards = ProgressCard.objects.all()
    paginator = Paginator(cards,3)
    card_number = request.GET.get('cards')
    card_obj = paginator.get_page(card_number)
    return render(request, 'web/progress.html', {
        "students" : students,
        "cards": cards,
        "card_obj" : card_obj
    })

def newCard (request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    task_name = request.POST["task_name"]
    description = request.POST["description"]
    status = request.POST["status"]
    attachment1 = request.FILES["attachment_1"]
    students_data = request.POST["students"]

    try:
        attachment2 = request.FILES['attachment_2']
    except:
        attachment2 = None

    
    cards = [card.strip() for card in students_data.split(",")]
    if not cards:
        return JsonResponse({
            "error": "At least one student required."
        }, status=400)

    # Convert email addresses to users
    students = []
    for username in cards:
        try:
            user = User.objects.get(username=username)
            students.append(user)
        except User.DoesNotExist:
            return JsonResponse({
                "error": f"User with username {username} does not exist."
            }, status=400)

    # Get contents of email
    
    
    card = ProgressCard(
            task_name=task_name,
            description=description,
            attachment_1 = attachment1,
            attachment_2 = attachment2,
            status = status,
        )
    card.save()
    card.students.set(students)
    card.save()
    
    return render (request, 'web/progress.html',
            {"message": "Card successfully created."}, status=201)


def card (request, card_id):
    # Query for requested email
    try:
        card = ProgressCard.objects.get(pk=card_id)
    except ProgressCard.DoesNotExist:
        return JsonResponse({"error": "Card not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(card.serialize())


    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("task_name") is not None:
            card.task_name = data["task_name"]
        if data.get("description") is not None:
            card.description = data["description"]
        if data.get("status") is not None:
            card.status = data["status"]
        if data.get("students") is not None:
            students_data = data['students']
            cards = [card.strip() for card in students_data.split(",")]
            card.students.set(User.objects.filter(username__in=cards))
        card.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


def personalCards (request, student_id): 
    cards = ProgressCard.objects.all()
    user = User.objects.get(pk=student_id)
    return render (request, 'web/personalcards.html', 
                   {"cards": cards,
                    "account": user})
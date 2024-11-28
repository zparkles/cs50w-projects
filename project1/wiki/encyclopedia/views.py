from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages
from . import util
import random

md = Markdown()



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, input):
    html_input= util.get_entry(input)
    converted = md.convert(html_input)
    return render(request, "encyclopedia/entry.html", {
        "converted": converted,
        "title": input
    })

def search_result(request):
    if request.method == "POST":
        searched = request.POST['q']
        searched_item= util.get_entry(searched)
        new_list = []
        if searched_item == None:
            for i in util.list_entries(): 
                if searched.lower() in i.lower():
                    new_list.append(i) 

            return render(request, "encyclopedia/search_results.html", {
                "list": new_list,
                "searched_item" : searched_item, 
                "searched": searched 
            })

        else:
            return HttpResponseRedirect("/wiki/%s/" %searched)
    return render(request, "encyclopedia/search_results.html")


def random_page(request):
    input = random.choice(util.list_entries())
    return HttpResponseRedirect("/wiki/%s/" %input)
    

class NewPageForms(forms.Form):
    title = forms.CharField(label= "Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":"1", "cols": "3"}), label="Content")
                            

def new_page(request):
    if request.method == "POST":
        form = NewPageForms(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) == None:
                util.save_entry(title, content)
                return HttpResponseRedirect("/wiki/%s/" %title)
            else:
                messages.info(request, 'Entry with the same title has already existed!')
                return render(request, "encyclopedia/new_page.html", {
                    "form": NewPageForms
                 })
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForms
    })



def edit_page(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content
        })
    elif request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect("/wiki/%s/" %title)  


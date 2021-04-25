from typing import Final
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, HttpResponse
import markdown2
import random
from django import forms
from . import util


# Form used to create a new entry/page
class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
            'placeholder': 'Enter title', 'id': 'new-entry-title','name':'title'}))
    data = forms.CharField(label="", widget=forms.Textarea(attrs={
        'id': 'new-entry','name':'data'}))


# controllers
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


#titlepage
def entryPage(request, title):
    markDownData = util.get_entry(title)
    if(markDownData == None):
        return render(request, "encyclopedia/invalidpage.html", {
            "title" : title
        })
    htmlData = markdown2.markdown(markDownData)
    return render(request, "encyclopedia/entry.html", {
        "title" : title,
        "html" : htmlData
    })

#searchpage
def search(request):
    matchedList = []
    searchQuery = request.POST.get("q")
    entries = util.list_entries()
    for item in entries:
        if item.upper() == searchQuery.upper():
            return HttpResponseRedirect(reverse("entrypage", args=[searchQuery]))
        if searchQuery.upper() in item.upper():
            matchedList.append(item)
    return render(request, "encyclopedia/searchresult.html", {
        "title": searchQuery,
        "list": matchedList
    })
    
def createEntry(request):
    if request.method == "POST":
        formData = NewPageForm(request.POST)
        if formData.is_valid():
            title = formData.cleaned_data['title']
            data = formData.cleaned_data['data']
            if(util.get_entry(title)!=None):
                return render(request, "encyclopedia/newpage.html", {
                    "newform" : NewPageForm(),
                    "error": "Such an entry already exists"
                })
            finalData = "#" + title + "\n" + data
            util.save_entry(title, finalData)
            return HttpResponseRedirect(reverse("entrypage", args=[title]))
    return render(request, "encyclopedia/newpage.html", {
        "title" : "Create Entry",
        "newform" : NewPageForm()
    })

def editEntry(request):
     if request.method == "GET":
         title = request.GET['title']
         data = util.get_entry(title)
         form = NewPageForm(initial={'title': title, 'data': data})
         return render(request, "encyclopedia/edit.html", {
             "title":"Edit data",
            "newform" : form
         })
     if request.method == "POST":
         formData = NewPageForm(request.POST)
         if formData.is_valid():
            title = formData.cleaned_data['title']
            data = formData.cleaned_data['data']
            if(util.get_entry(title)!=None):
                util.save_entry(title, data)
                return HttpResponseRedirect(reverse("entrypage", args=[title]))

def randomPage(request):
    entries = util.list_entries()
    value = random.choice(entries)
    return HttpResponseRedirect(reverse("entrypage", args=[value]))
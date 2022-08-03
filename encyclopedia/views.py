
from django.http import HttpResponse
from logging import PlaceHolder
from django.shortcuts import render
from django import forms

import random
from . import util
import markdown



class NewSearchForm(forms.Form):
    query = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class CreateForm(forms.Form):
    title = forms.CharField(label = "title", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    text =  forms.CharField(label = "text",  widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder':"Content"}))
class EditForm(forms.Form):
    text =  forms.CharField(label = "text",  widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder':"Content"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : NewSearchForm()
    })
def entry(request, name):
    entryValue = util.get_entry(name)
    if entryValue is None:
        entryHtml = f"{name.capitalize()} is not Found. Please try another entry value. "
    else:
        entryHtml =  markdown.markdown(entryValue)

    
    return render(request, "encyclopedia/entry.html", {
        "entryHtml": entryHtml,
        "entryName": name,
        "form" : NewSearchForm()

    })

def search(request):
    if request.method == "POST":
        entries = util.list_entries()
        form = NewSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            entryValue = util.get_entry(query)
            if entryValue is None:
                output = [entry for entry in entries if query in entry]     
                return render(request, "encyclopedia/searchVals.html", {
                    'entries' : output,
                    "form" : NewSearchForm(), 
                    'query': query
                })
            else:
                entryHtml =  markdown.markdown(entryValue)
                return render(request, "encyclopedia/entry.html", {
                    "entryHtml": entryHtml,
                    "entryName": query,
                    "form" : NewSearchForm()
                })          
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : NewSearchForm()
    })

def createpage(request):
    if 'save' in request.POST:
        entries = util.list_entries()
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["text"]
            if title not in entries:
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html", {
                    "entryHtml" : markdown.markdown(util.get_entry(title)),
                    "entryName" : title,
                    "form" : NewSearchForm()
                    })

            else: 
                return render(request, "encyclopedia/entry.html", {
                "entryHtml": "The page you're creating already exists",
                "entryName": title,
                "form" : NewSearchForm()
                 })
    elif 'search' in request.POST:
        search(request)

    return render(request, "encyclopedia/createpage.html", {
        "form2" : CreateForm(),
        "form" : NewSearchForm()
    })
def edit(request,name):
    entryValue = util.get_entry(name)
    if 'save' in request.POST:
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["text"]
            util.save_entry(name, content)
            return render(request, "encyclopedia/entry.html", {
                "entryHtml" : markdown.markdown(util.get_entry(name)),
                "entryName" : name,
                "form" : NewSearchForm()
                })

    elif 'search' in request.POST:
        search(request)

    return render(request, "encyclopedia/edit.html", {
        "form2" : EditForm({"text":entryValue}),
        "form" : NewSearchForm(),
        "entry": name
    })
def randompage(request):
    entries = util.list_entries()
    name = random.choice(entries)
    return entry(request,name)

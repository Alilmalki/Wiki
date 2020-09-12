from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entrytitle):
    if util.get_entry(entrytitle) is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry": util.get_entry(entrytitle),
            "entrytitle": entrytitle
        })
    else:
        return render(request, "encyclopedia/error.html")

def search(request):
    if(request.method == "POST"):
        title = request.POST["q"]
        if util.get_entry(title) is not None:
            return entry(request, title)

    entries = util.list_entries()
    matching = []

    for x in entries:
        if x.lower().find(title.lower()) != -1:
            matching.append(x)
    
    if len(matching) == 0:
        
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/matching.html", {
            "results": matching
        })

def add(request):
    if(request.method == "POST"):
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "encyclopedia/add.html")

def edit(request, entrytitle):
    print(entrytitle)
    if(request.method == "POST"):
        content = request.POST["content"]
        print(entrytitle)
        util.save_entry(entrytitle, content)
        return HttpResponseRedirect(reverse("index"))
    
    
    entry = util.get_entry(entrytitle)
    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "entrytitle": entrytitle
    })
def random(request):
    entries = util.list_entries()
    selected_entry = random.choice(entries)
    
    return redirect("entry", {
        "entry": selected_entry
    })

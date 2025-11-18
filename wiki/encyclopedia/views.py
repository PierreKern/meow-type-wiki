from django.shortcuts import render
import markdown
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return(markdowner.convert(content))

def entry(request, title):
    content = md_to_html(title)
    if content == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content 
        })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    content = md_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": content
    })
    
def search(request):
    if request.method == "POST":
        entry_search = request.POST.get('q', '').strip()
        content = md_to_html(entry_search)
        if content:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": content
            }) 
        entries = util.list_entries()
        closed_entries = [
            entry for entry in entries if entry_search.lower() in entry.lower()
        ]
        return render(request, "encyclopedia/search.html", {
            "closed_entries": closed_entries,
            "search_entry": entry_search
        })

def create_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        is_title_exist = util.get_entry(title)
        if is_title_exist != None:
            return render(request, "encyclopedia/error.html")
        else:
            util.save_entry(title, content)
            content = md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                title: title,
                "content": content
            })

def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            title: title,
            "content": content
        })


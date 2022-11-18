from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost

# Create your views here.
def index(request):
    blogs = Blogpost.objects.all()
    return render(request, "blog/index.html", {"blogs": blogs})

def blogpost(request, id):
    blogpost = Blogpost.objects.filter(post_id = id)[0]
    #allBlogsLen = len(Blogpost.objects.all())
    PrevId = blogpost.post_id - 1
    nextId = blogpost.post_id + 1
    return render(request, "blog/blogpost.html", {"post": blogpost, "PrevId": PrevId, "nextId": nextId})
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post

def post_list(request):
    posts = Post.published.all()
    return render(request,'blog/post/list.html',{'posts': posts})

from django.http import Http404

def post_detail(request, id):
    #try:
    #    post = Post.objects.filter(status = Post.Status.PUBLISHED).get(id=id)
    #except Post.DoesNotExist:
    #    raise Http404('No post found')
    #using get_object_or_404 instead of DoesNotExist error
    post = get_object_or_404(Post,id=id,status = Post.Status.PUBLISHED)
    
    return render(request,'blog/post/detail.html',{'post': post})
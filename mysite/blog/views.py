from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, BlogPostForm, LoginForm
from django.core.mail import send_mail
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.views.generic import ListView # Allow to list any type of objects
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from PIL import Image

# function based post list view
'''def post_list(request):
    post_list = Post.published.all()
    
   # pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    # 1. handling emptypage/page out of range error
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # if page_number is out of range, deliver last page of the results
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # if page is not an interger deliver first page
        posts = paginator.page(1)
   # normal posts = paginator.page(page_number)
    return render(request,'blog/post/list.html',{'posts': posts})'''

# Class Based Post_List View
class PostListView(ListView):
    queryset = Post.published.all() # or model = Post to use the generic manager Post.objects.all()
    context_object_name = 'posts' # default name is object_list
    paginate_by = 3 # defines pagination
    template_name = 'blog/post/list.html'
    
from django.http import Http404

def post_detail(request, year, month, day,post):
    #try:
    #    post = Post.published.get(id=id)
    #except Post.DoesNotExist:
    #    raise Http404('No post found')
    #using get_object_or_404 instead of DoesNotExist error
    post = get_object_or_404(Post,status = Post.Status.PUBLISHED,
                             slug=post,
                             publish__year = year,
                             publish__month = month,
                             publish__day = day,
                             )
    
    
    comments = post.comments.filter(active = True) # list of active comments for this post
    form = CommentForm()
    
    return render(request,'blog/post/detail.html',{'post': post,
                                                   'comments': comments,
                                                   'form': form})

@login_required
def upload_post(request):

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
           post = form.save(commit = False)
           post.author = request.user #assignig author to be the user
           post.save()
           
           
         
    else:
        form = BlogPostForm()
    return render(
        request, 'blog/post/upload_post.html',{'form':form}
    )


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
               
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})


# Sharing posts via email
from .forms import EmailPostForm

def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status = Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
           # form fields passed validation
          cd = form.cleaned_data 
          post_url = request.build_absolute_uri(post.get_absolute_url()) # building complete url
          subject = f"{cd['name']} recommends you to read {post.title}"
          message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
          send_mail(subject, message,'nicholas2541001@gmail.com',[cd['to']])
          sent = True # use it later in a template to display a scuccess message when the form is successfully submitted
        
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post' : post,
                                                    'form' : form,
                                                    'sent': sent})

@require_POST # allows POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,id = post_id, status = Post.Status.PUBLISHED
                             )
    comment = None
    form = CommentForm(data = request.POST) # a comment was posted
    if form.is_valid():
        comment = form.save(commit=False)#create a comment object without saving to the database
        comment.post = post # assign the post to the comment
        comment.save()
    return render(request,'blog/post/comment.html',
                  {'post':post,
                   'form':form,
                   'comment':comment})
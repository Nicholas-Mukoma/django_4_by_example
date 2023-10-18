from django import forms
from .models import Comment, Post

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length = 25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required = False, widget = forms.Textarea)

#A form to let users comment on blog posts   
class CommentForm(forms.ModelForm):
    class Meta:
       model = Comment # indicating which model to build the form from
       fields = ['name','email','body'] # explicitly telling djando which fields to include

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','image']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
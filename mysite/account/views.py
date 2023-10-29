from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm , UserRegistrationForm,UserEditForm, ProfileEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile

#function based login view
'''def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, #checks user credantials and returns a user object.
                                username = cd['username'],
                                password = cd['password'])
            
            if user is not None: # checks if the user has been authenticated
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')

    else:
        form = LoginForm()
    return render(request,'account/login.html', {'form':form})'''

#if user is authenticated it executes this view.if not, user is redirected to the user login URL
#with the originally requested URL as a GET parameter named next
#by doing this, login view redirects users to the URL,they were trying to accesss after they successfully log in. This works due to the hidden <input> named next in the login template
@login_required
def dashboard(request):
    profile = Profile.objects.filter(user= request.user)
    return render(request,'account/dashboard.html',{'section':'dashboard','profile':profile}) # this section variable is to highlight the current section of the main menu of the site

#view for creating user accounts
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object without saving it yet
            new_user = user_form.save(commit= False)
            # we then set the choosen password.set_password handles password hashing b4 storing to the data base
            new_user.set_password(user_form.cleaned_data['password'])
            # we now save the user object
            new_user.save()
            #create the user profile.when user registers, a profile object is created associated
            #with the User object created
            Profile.objects.create(user = new_user)

            return render(request,'account/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files = request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,'account/edit.html',{'user_form':user_form,'profile_form': profile_form})
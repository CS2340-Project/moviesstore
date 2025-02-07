from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from . import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.models import User

def forgot_password(request):
    template_data = {}
    template_data['title'] = 'Forgot Password'

    if request.method == 'POST':
        username = request.POST.get('username')
        security_answer = request.POST.get('security_answer')
        
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            
            # Always set the security question when username is found
            template_data['security_question'] = user_profile.security_question
            
            # Only check the answer if it was provided
            if security_answer:
                if user_profile.security_answer.lower() == security_answer.lower():
                    request.session['reset_user_id'] = user.id
                    return redirect('accounts.reset_password')
                else:
                    template_data['error'] = 'Incorrect security answer'
                    template_data['show_answer'] = True
            else:
                template_data['show_answer'] = True
                
        except User.DoesNotExist:
            template_data['error'] = 'User not found'
        except UserProfile.DoesNotExist:
            template_data['error'] = 'Security question not set for this user'
    
    return render(request, 'accounts/forgot_password.html',
        {'template_data': template_data})
def reset_password(request):
    template_data = {}
    template_data['title'] = 'Reset Password'

    if 'reset_user_id' not in request.session:
        return redirect('accounts.login')  # Updated to match URL pattern
        
    if request.method == 'POST':
        form = forms.ResetPasswordForm(request.POST, error_class=forms.CustomErrorList)
        if form.is_valid():
            user = User.objects.get(id=request.session['reset_user_id'])
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            
            del request.session['reset_user_id']
            messages.success(request, 'Password has been reset successfully')
            return redirect('accounts.login')  # Updated to match URL pattern
        else:
            template_data['form'] = form
    else:
        template_data['form'] = forms.ResetPasswordForm()
    
    return render(request, 'accounts/reset_password.html',
        {'template_data': template_data})

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    
    if request.method == 'GET':
        template_data['form'] = forms.CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})

    elif request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST, error_class=forms.CustomErrorList)
        if form.is_valid():
            user = form.save()
            # Create the UserProfile with security question
            UserProfile.objects.create(
                user=user,
                security_question=form.cleaned_data['security_question'],
                security_answer=form.cleaned_data['security_answer']
            )
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})
        
def login(request):
    template_data = {}
    template_data['title'] = 'Sign In'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                          {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
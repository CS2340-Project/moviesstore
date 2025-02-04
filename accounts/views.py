from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms

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
            form.save()
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
def logout(request):
    auth_logout(request)
    return redirect('home.index')
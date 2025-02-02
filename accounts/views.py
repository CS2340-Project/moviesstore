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
            return redirect('home.index')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})
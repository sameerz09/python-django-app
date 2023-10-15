from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/test/')  # Redirect to '/test/' upon successful login
        else:
            return HttpResponse("Invalid login credentials")  # Handle login failure
    return render(request, 'login.html')  # Render the login form

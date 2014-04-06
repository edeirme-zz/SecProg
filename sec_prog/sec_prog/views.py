from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(Name=username, Password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            return render(request, 'main.html')
    else:
        return render(request, 'main.html')

@login_required(login_url='/')
def shop(request):
    return render(request, 'shop.html')

@login_required
def logout_view(request):
    logout(request)
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from shop.models import Shop
from django.http import HttpResponse
import json

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
    products = Shop.objects.all()

    return render_to_response('shop.html', {'products': products}, context_instance=RequestContext(request))


def build_blog_movie(request):
    test = request.POST.get("blogTitle", "")
    response_data = {}
    response_data['result'] = 'Writing the blog was a success'
    response_data['message'] = test



    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def logout_view(request):
    logout(request)
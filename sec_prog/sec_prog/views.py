from django.shortcuts import render, render_to_response
from django.template import RequestContext, Context
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from shop.models import Shop
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.template.loader import get_template
import json


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(Name=username, Password=password)
    if user is not None:
        if user.is_active:
            request.session['is_logged'] = True
            login(request, user)
        else:
            return render(request, 'main.html')
    else:
        return render(request, 'main.html')


@login_required(login_url='/')
def shop(request):
    products = Shop.objects.all()
    return render_to_response('shop.html', {'products': products}, context_instance=RequestContext(request))


@login_required(login_url='/')
def checkout(request):
    return render_to_response('checkout.html', context_instance=RequestContext(request))


@login_required
def logout_view(request):
    logout(request)

@login_required(login_url='/')
def proceedOrder(request):
    test = []
    products = []
    username = None
    username = request.user.username
    delivery_address = request.POST.get('delivery_address', '')
    #Get Post length so we can iterate through the array
    length = request.POST.get('length', '')
    #iterate through the array and store the product to the array "products"
    for i in range(int(length)):
        test.append(request.POST.getlist("product_array[" + str(i) + "][]"))
        if Shop.objects.filter(pk=int(test[i][2])).exists():
            products.append(Shop.objects.get(pk=int(test[i][2])))
    #Send Email
    mail_template = get_template('email.html')
    c = RequestContext(request, {'products': products, 'address': delivery_address, 'username': username})
    send_mail('Report', mail_template.render(c), 'console@exapmple.com',
              ['admin@example.com'], fail_silently=False)
    #Continue with ajax
    response_data = {}
    try:
        response_data['result'] = 'Writing the blog was a success!'
        response_data['message'] = 'Your order has been sent'
    except:
        response_data['result'] = 'Oh noes!'
        response_data['message'] = 'The subprocess module did not run the script correctly!'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

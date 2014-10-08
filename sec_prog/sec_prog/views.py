from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from shop.models import Shop, Cart, User_Votes
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.contrib.auth.models import User
import json
import re


@login_required(login_url='/')
def shop(request):
    products = Shop.objects.all()

    for i in range(len(products)):
        try:

            products[i].stars= products[i].stars/products[i].votes

            if products[i].stars > 5:
                products[i].stars = 5
        except:
            products[i].stars= 0

    request.session['view'] = 'shop';
    return render_to_response('shop.html', {'products': products}, context_instance=RequestContext(request))


@login_required(login_url='/')
def checkout(request):
    cart_products = Cart.objects.filter(user_id=request.user.id)
    cart = []
    # for i in range(len(cart_products)):
    #     cart.append(cart_products[i].item_id)
    # all_products = Shop.objects.filter(id__in=cart)
    user_cart = [[ 0 for i in xrange(8)] for x in xrange(len(cart_products))]
    total_cost = 0
    num_of_products = 0
    request.session['view'] = 'checkout';
    for i in range(len(cart_products)):
        user_cart[i][0] = cart_products[i].qnty
        tmp = Shop.objects.get(id=cart_products[i].item_id_id)
        user_cart[i][1] = tmp.product_name
        user_cart[i][2] = tmp.price
        user_cart[i][3] = cart_products[i].item_id_id
        user_cart[i][4] = tmp.description
        try:
            user_cart[i][5] = (tmp.stars / tmp.votes)
        except:
            user_cart[i][5] = 0
        user_cart[i][6] = tmp.imagename
        try:
            tmp2 = User_Votes.objects.get(user_id=request.user.id, item_id=cart_products[i].item_id)
            # user_cart[i][7] = 1
        except:
            tmp2 = None
        user_cart[i][7] = (tmp2 is None)
        num_of_products = num_of_products + cart_products[i].qnty
        total_cost = total_cost + (tmp.price*cart_products[i].qnty)
        #user_cart[i].product_name = all_products[i].product_name
        # user_cart[i].price = all_products[i].price
        # user_cart[i].quantity = cart_products[
    # with open("/home/kirios/Desktop/test.txt", "a") as myfile:
    #     myfile.write(str(all_products))
    return render_to_response('checkout.html',{'products': user_cart, 'total_cost':total_cost, 'num_of_products':num_of_products}, context_instance=RequestContext(request))


@login_required
def logout_view(request):
    logout(request)

@login_required(login_url='/')
def proceedOrder(request):
    test = []
    cart_products = []
    products = []
    username = None
    username = request.user.username
    user = request.user
    delivery_address = request.POST.get('delivery_address', '')
    #Get Post length so we can iterate through the array
    tmp = []
    request.session['view'] = 'checkout'
    cart_products = Cart.objects.filter(user_id=user)
    for i in range(len(cart_products)):
        tmp = Shop.objects.get(id=cart_products[i].item_id_id)
        products.append(tmp.product_name)

    #Send Email
    mail_template = get_template('email.html')
    c = RequestContext(request, {'products': products, 'address': delivery_address, 'username': username})
    send_mail('Report', mail_template.render(c), 'console@exapmple.com',
              ['admin@example.com'], fail_silently=False)
    #Continue with ajax

    Cart.objects.filter(user_id=user).delete()
    response_data = {}
    try:
        response_data['result'] = 'Writing the blog was a success!'
        response_data['message'] = 'Your order has been sent'
    except:
        response_data['result'] = 'Oh noes!'
        response_data['message'] = 'The subprocess module did not run the script correctly!'

    return HttpResponse(json.dumps(response_data), content_type="application/json")





@login_required(login_url='/')
def search_product(request):
    products = []
    search_input = request.POST.get('search_input', '')
    try:
        products = Shop.objects.filter(product_name__icontains=search_input)
    except:
        products = None
    for i in range(len(products)):
        try:

            products[i].stars= products[i].stars/products[i].votes
            if products[i].stars > 5:
                products[i].stars = 5
        except:
            products[i].stars= 0
    try:
        response_data = {'result': 'Writing the blog was a success', 'message': product_array, 'array_length': len(products)}
    except:
        response_data = {'result': 'Oh noes', 'message': 'The subprocess module did  not run the script correctly', 'array_length': 0}


    return render_to_response('container.html', {'products': products}, context_instance=RequestContext(request))


@login_required(login_url='/')
def add_to_cart(request):
    user = request.user
    itemID = int(request.POST.get('itemID', 0))
    quantity = int(request.POST.get('qnty', 0))
    request.session['view'] = 'shop';

    try:
        item = Shop.objects.get(id=itemID)
    except:
        item = None

    cart = []
    try:
    #if len(Cart.objects.all()) > 0:
        cart = Cart.objects.get(item_id=itemID,user_id=user)
        cart.qnty=cart.qnty+quantity
    except Cart.DoesNotExist:
        cart = None
        cart = Cart(user_id=user, item_id=item, qnty=quantity)


    cart.save()
    response_data = {}


    try:
        response_data['result'] = 'Ok'
    except:
        response_data['result'] = 'not ok'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/')
def remove_item(request):
    user = request.user
    itemID = int(request.POST.get('itemID', ''))
    total_cost = float(request.POST.get('total_cost', ''))
    product_price = float(request.POST.get('product_price', ''))
    qnty = int(request.POST.get('qnty', ''))
    total_cost = total_cost - (product_price*float(qnty))
    request.session['view'] = 'checkout';
    num_of_products = 0
    try:
        Cart.objects.filter(item_id=itemID,user_id=user).delete()
        cart_products = Cart.objects.filter(user_id=user)
        for i in range(len(cart_products)):
            num_of_products = num_of_products + cart_products[i].qnty


    except:
        la=1

    response_data = {}
    response_data['total_cost'] = total_cost
    response_data['num_of_products'] = num_of_products
    try:
        response_data['result'] = 'Ok'
    except:
        response_data['result'] = 'not ok'
    return HttpResponse(json.dumps(response_data), content_type="application/json")



@login_required(login_url='/')
def update_cart(request):
    user = request.user
    products = []
    length = int(request.POST.get('length',0))
    request.session['view'] = 'checkout';
    for i in range(length):
        products.append([request.POST.getlist("product_array[" + str(i) + "][product_id]"),
                    request.POST.getlist("product_array[" + str(i) + "][price]"),
                    request.POST.getlist("product_array[" + str(i) + "][qnty]")])

    for i in range(length):
        cart =[]
        try:
            cart = Cart.objects.get(item_id=int(products[i][0][0]),user_id=user)
        except Cart.DoesNotExist:
            cart = None
        cart.qnty = int(products[i][2][0])
        if cart.qnty > 0:
            cart.save()
        else:
            Cart.objects.filter(item_id=int(products[i][0][0]),user_id=user).delete()

    cart_products = Cart.objects.filter(user_id=request.user)
    #cart = []
    # for i in range(len(cart_products)):
    #     cart.append(cart_products[i].item_id)
    # all_products = Shop.objects.filter(id__in=cart)
    user_cart = [[ 0 for i in xrange(5)] for x in xrange(len(cart_products))]
    num_of_products = 0
    total_cost = 0
    for i in range(len(cart_products)):
        user_cart[i][0] = cart_products[i].qnty
        tmp = Shop.objects.get(id=cart_products[i].item_id_id)
        user_cart[i][1] = tmp.product_name
        user_cart[i][2] = tmp.price
        user_cart[i][3] = cart_products[i].item_id_id
        user_cart[i][4] = tmp.description
        total_cost = total_cost + (tmp.price*cart_products[i].qnty)
        num_of_products = num_of_products + cart_products[i].qnty


    response_data = {}
    try:
        response_data = {'result': 'Ok', 'message': user_cart, 'total_cost':total_cost, 'array_length': len(user_cart), 'num_of_products':num_of_products}
    except:
        response_data = {'result': 'not Ok', 'message': 'Error', 'total_cost':0, 'array_length': 0, 'num_of_products':0}
    return HttpResponse(json.dumps(response_data), content_type="application/json")



@login_required(login_url='/')
def rate_product(request):
    user = request.user
    user_rating = int(request.POST.get('user_rating', ''))
    product_id = int(request.POST.get('product_id',''))
    request.session['view'] = 'checkout';

    try:
        temp = Shop.objects.get(id=product_id)
        temp2 = User_Votes(user_id=user, item_id=temp)
        temp2.save()

        temp.stars = temp.stars + user_rating
        temp.votes = temp.votes + 1
        temp.save()

    except Shop.DoesNotExist:
        temp = None
    response_data = {}
    try:
        response_data = {'result': 'Ok', 'rating': (temp.stars/temp.votes)}
    except:
        response_data = {'result': 'not Ok', 'rating':0}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/')
def settings(request):
    return render_to_response('settings.html', context_instance=RequestContext(request))


@login_required(login_url='/')
def change_pass(request):
    user = request.user
    new_pass = request.POST.get('new_pass','')

    user.set_password(new_pass)
    user.save()
    request.session['view'] = 'settings';
    response_data = {}
    try:
        response_data = {'result': 'Ok'}
    except:
        response_data = {'result': 'not Ok'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/')
def syncsearch(request):

    if request.method == 'POST':
        request.session['view'] = 'shop';
        products = []
        search_input = request.POST.get('search_input', '')
        try:
            products = Shop.objects.filter(product_name__icontains=search_input)
        except:
            products = None
        for i in range(len(products)):
            try:

                products[i].stars= products[i].stars/products[i].votes
                if products[i].stars > 5:
                    products[i].stars = 5
            except:
                products[i].stars= 0
        try:
            response_data = {'result': 'Writing the blog was a success', 'message': product_array, 'array_length': len(products)}
        except:
            response_data = {'result': 'Oh noes', 'message': 'The subprocess module did  not run the script correctly', 'array_length': 0}

    else:
        products = None
    return render_to_response('shop.html', {'products': products}, context_instance=RequestContext(request))

from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import *
from adminapp.models import*
from.models import*

#PAYMENT INTEGRATION
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
stripe.api_key = settings.STRIPE_SECRET_KEY



# Dashboard
def userdash(request):
    if 'userid' not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect('login')

    userid = request.session['userid']
    user = Userinfo.objects.get(email=userid)

    return render(request, "userdash.html", {'userid': userid, 'user': user})


# Logout
def userlogout(request):
    if 'userid' in request.session:
        del request.session['userid']
        messages.success(request, "You are logged out successfully.")
    else:
        messages.warning(request, "Something went wrong.")

    return redirect('index')


# View Profile
def userprofile(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to view your profile.")
        return redirect('login')

    userid = request.session['userid']
    user = Userinfo.objects.get(email=userid)
    context={
        'userid':userid,
        'user' : user
    }
    return render(request, "userprofile.html", context)


# Edit Profile
def editprofile(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to edit your profile.")
        return redirect('login')

    userid = request.session['userid']
    user = Userinfo.objects.get(email=userid)

    context={
        'userid':userid,
        'user' : user
    }
    
    if request.method  == "POST":
        name = request.POST.get('name')
        contactno=request.POST.get('contactno')
        picture=request.FILES.get('profile')
        address=request.POST.get('address')
        user.name=name
        user.contactno=contactno
        if picture:
            user.picture = picture
        user.address=address
        user.save()
        messages.success(request, "Your Profile has been Updated")
        return redirect('userprofile')

    return render(request, "editprofile.html", context)


# View Cart
def viewcart(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to view your cart.")
        return redirect('login')

    userid = request.session['userid']
    user = Userinfo.objects.get(email=userid)

    ucart = Cart.objects.filter(user=user)
    if not ucart:
        Cart.objects.create(user=user)
    cart = Cart.objects.get(user=user)
    items = CartItem.objects.filter(cart=cart)#['book1'2, 'book2'1]
    total_price=0
    for i in items:
        total_price += i.get_total_price()

    context = {

        'userid' : userid,
        'user' : user,
        'items': items,
        'total_price' :total_price,

    }

    return render(request, "viewcart.html", context)


# Orders
def userorders(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to view your orders.")
        return redirect('login')

    userid = request.session['userid']
    user = Userinfo.objects.get(email=userid)
    orders = Order.objects.filter(user=user).order_by('-ordered_at')
    orderitems = [] #list of lists [[order1items], [order2items] ]
    for order in orders:
        orderitems.append(OrderItem.objects.filter(order=order))

    context = {
        'userid': userid,
        'user': user,
        'orders': orders,
        'orderitems': orderitems,
    }

    return render(request, "userorders.html", context)

     
# Change Password
def userpass(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to change your password.")
        return redirect('login')

    userid = request.session['userid']
    user = Userinfo.objects.get(email=userid)

    return render(request, "userpass.html", {'userid': userid, 'user': user})

def addtocart(request,bid):
    if not 'userid' in request.session:
        messages.error(request, "You are not logged in")
        return redirect('login')
    userid = request.session.get('userid')
    user = Userinfo.objects.get(email=userid)
    ucart = Cart.objects.filter(user=user)
    if not ucart:
        Cart.objects.create(user=user)
    cart = Cart.objects.get(user=user)
    book = Book.objects.get(id=bid)
    if request.method == "POST":

        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity) if quantity else 1
        except (TypeError, ValueError):
            quantity = 1
        ci = CartItem.objects.filter(cart=cart, book=book)
        if ci:
            item = ci.first()
            item.quantity += quantity
            item.save()
        else:
            CartItem.objects.create(cart=cart, book=book, quantity=quantity)
        messages.success(request, f"{book.title} is added to cart")
        return redirect('viewcart')
    else:
        messages.error(request,"Something Went wrong ")
        return redirect('index')
    
    
def removeitem(request, cid):
    if not 'userid' in request.session:
        messages.error(request, "You are not logged in")
        return redirect('login')
    userid = request.session.get('userid')
    user = Userinfo.objects.get(email=userid)
    ci = CartItem.objects.filter(id=cid)
    ci.delete()
    messages.success(request, "Item removed from cart")
   
    return redirect('viewcart')

def updateitem(request,id,operator):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged In!!")
        return redirect('login')
    userid = request.session.get('userid')
    user = Userinfo.objects.get(email=userid)
    ci = CartItem.objects.filter(id=id)
    if operator == "+":
        ci.quantity += 1
        if ci.book.stock < ci.quantity:
            messages.warning(request, "Item quantiy is exceded than stock.")
            return redirect('viewcart')
    elif operator == "-":
        ci.quantity -= 1
        if ci.quantity == 0:
            ci.delete()
            messages.warning(request,"Removed")
            return redirect('viewcart')
    ci.save()
    messages.success(request, "Item Quantity updated successfully.")
    return redirect('viewcart')


def checkout(request):
    if 'userid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    userid = request.session.get('userid')
    user = Userinfo.objects.get(email=userid)
    cart = Cart.objects.get(user=user)
    items = CartItem.objects.filter(cart=cart)

    line_items = []

    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'unit_amount': int(item.book.price * 100),
                'product_data': {
                    'name': item.book.title,
                },
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card', 'sepa_debit'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/userapp/payment-success/'),
        cancel_url=request.build_absolute_uri('/viewcart/'),
    )

    return redirect(session.url, code=303)


def payment_success(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login first.")
        return redirect('login')

    userid=request.session.get('userid')
    user = Userinfo.objects.get(email=userid)

    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            messages.warning(request, "No items found in your cart.")
            return redirect('index')

  
        total_amount = sum(item.get_total_price() for item in cart_items)
        order = Order.objects.create(user=user, total_amount=total_amount)

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            )
            book = Book.objects.get(id = item.book.id)
            book.stock = book.stock - item.quantity
            book.save()

        cart_items.delete()

        items = OrderItem.objects.filter(order=order)

        # Add total_price attribute to each item
        for item in items:
            item.total_price = item.quantity * item.price

        
        messages.success(request, "Payment successful! Your order has been placed.")
        return render(request, 'payment_success.html', {'order': order})

    except Cart.DoesNotExist:
        messages.error(request, "Cart not found.")
        return redirect('index')

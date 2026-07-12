from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from .models import *

# Create your views here.
def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request, "you are not logged in .")
        return redirect ('adminlogin')
    adminid = request.session.get('admin')
    context = {
        'adminid' : adminid,


    }

    return render(request, 'admindash.html',context)

def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request, 'you are logged out.')
    else:
        messages.error(request,'something going went wrong')
        return redirect('index')
    
def addcat(request):
    if not 'adminid' in request.session:
        messages.error(request, "you are not logged in .")
        return redirect ('adminlogin')
    adminid = request.session.get('admin')
    context = {
        'adminid' : adminid
    }
    if request.method == 'POST':
        name= request.POST.get('name')
        description = request.POST.get('description') 
        check = Category.objects.filter(name=name, description=description)
        if check:
            messages.warning(request, "Category already exits")
            return redirect('addcat')
        Category.objects.create(name=name, description=description)
        messages.success(request, "Categoru added successfully")
        return redirect('addcat')

    return render(request, 'addcat.html', context)

def viewcat(request):
    if not 'adminid' in request.session:
        messages.error(request, "you are not logged in .")
        return redirect ('adminlogin')
    adminid = request.session.get('admin')
    context = {
        'adminid' : adminid
    }
    return render(request, 'viewcat.html', context)

def changepassword(request):
    if not 'adminid' in request.session:
        messages.error(request, "you are not logged in .")
        return redirect ('adminlogin')
    adminid = request.session.get('admin')
    context = {
        'adminid' : adminid
    }
    return render(request, 'changepassword.html', context)


def addbook(request):
    if not 'adminid' in request.session:
        messages.error(request, "you are not logged in .")
        return redirect ('adminlogin')
    adminid = request.session.get('admin')
    categories = Category.objects.all()

    context = {
        'adminid' : adminid,
        'categories' : categories
    }
    if request.method == "POST":
        title =request.POST.get('title')
        author =request.POST.get('author')
        catid =request.POST.get('catid')
        cat =Category.objects.get(id =catid)
        # catogory = cat,
        description = request.POST.get('description')
        original_price = request.POST.get('original_price')
        price = request.POST.get('price')
        published_date = request.POST.get('publish_date')
        language = request.POST.get('language')
        cover_image = request.FILES.get('cover_image')
        stock = request.POST.get('stock')
        Book.objects.create(
            title=title, author=author, category=cat, description=description,original_price=original_price, price=price, published_date=published_date,language=language,cover_image=cover_image,stock=stock
        )
        messages.success(request, "new  book added successfully")
        return redirect('addbook')
    
    return render(request, 'addbook.html', context)


def viewbook(request):
    if not 'adminid' in request.session:
        messages.error(request, "you are not logged in .")
        return redirect ('adminlogin')
    adminid = request.session.get('admin')
    context = {
        'adminid' : adminid
    }
    return render(request, 'viewbokk.html', context)

def enquiry(request):
    if not 'adminid' in request.session:
        messages.error(request, "you are not logged in .")
        return redirect ('adminlogin')
    adminid = request.session.get('admin')
    enqs = Enquiry.objects.all()
    context = {
        'adminid' : adminid,
        'enqs': enqs
    }
    return render(request, 'enquiry.html', context)

def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are Not logged in.")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context={
        'adminid':adminid,
        'user_count':Userinfo.objects.all().count(),
        'book_count':Book.objects.all().count(),
        'cat_count':Category.objects.all().count(),
        # 'order_count':Order.objects.all().count(),
        'enqs_count':Enquiry.objects.all().count(),
        # 'total_revenue':total_revenue,
    }
    return render(request,"admindash.html",context)
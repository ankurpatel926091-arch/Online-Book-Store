from django.shortcuts import render, redirect
from.models import *
from django.contrib import messages
from adminapp.models import *
# Create your views here.
def index(request):
   userid = request.session.get('userid')
   books = Book.objects.all()
   context = {
      'books':books,
      'userid' : userid,
      
   }
   return render(request,'index.html',context)

def about(request):
   userid = request.session.get('userid')
   context = {
      'userid' : userid,
   }
   return render(request,'about.html',context)

def login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user = LoginInfo.objects.get(usertype="user",username=username,password=password)
            if user is not None:
                messages.success(request,"Welcome user")
                request.session['userid'] = user.username
                return redirect('userdash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"invalid credentials")
            return redirect('index')
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        contactno=request.POST.get('contactno')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        Enquiry.objects.create(name=name,email=email, contactno=contactno,subject=subject)
        messages.success(request,"enquiry had been submitted successfully.")
        return redirect ('contact')
    return render(request,'contact.html')
# def adminlogin(request):
#     return render(request,"login.html")

def register(request):
    if request.method == "POST":
     name = request.POST.get  ('name')
     email = request.POST.get  ('email')
     contactno = request.POST.get  ('contactno')
     password= request.POST.get  ('password')
     cpassword = request.POST.get  ('cpassword')
     if password !=cpassword:
        messages.warning(request,"password and confirm passwordf do not matched.")
        return redirect ('register')
     check = LoginInfo.objects.filter(username=email)
     if check:
        messages.warning(request,"This email is already registered")
        return redirect('register')
     log = LoginInfo( username=email, password=contactno)
     user = Userinfo(login=log,name = name, email = email, contactno = contactno,)
     log.save()
     user.save()
     
     
    return render(request,"register.html")

def adminlogin(request):
    if request.method == "POST":
     username =request.POST.get('username')
     password =request.POST.get('password')
     try:
         admin = LoginInfo.objects.get(usertype="admin",username=username ,password=password)
         if admin is not None:
            messages.success(request, 'welcome admin')
            request.session['adminid'] = admin.username
            return redirect('admindash')

     except LoginInfo.DoesNotExist:
         messages.error(request,'invalid cridentials')
         return redirect('adminlogin')                                          
    return render(request,"adminlogin.html" )

def book_details(request, id ):
   book = Book.objects.get(id=id)
   context = {
      'book':book,
   }
   return render(request , "book_details.html",context)

from django.shortcuts import render

def about(request):
    return render(request, 'about.html')

      


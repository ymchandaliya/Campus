import json
import requests
import secrets
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
# from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.urls import reverse_lazy
from .models import *
from CMP.settings import EMAIL_HOST_USER
from verify_email.email_handler import send_verification_email
from django.core.mail import send_mail
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import time
# Create your views here.

def home(request):
    if request.method == 'GET':
        return render(request, 'homepage.html')

# def signup(request):
#     return render(request,'signup.html',context = {'x':0})

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html',context = {'x':0})

    elif request.method == 'POST':
        try:
            print("signup")
            enroll1 = request.POST['enroll']
            print(enroll1)
            # enroll = request.form.get("inputEnroll")
            u = CollegeData.objects.get(enroll=enroll1)
            print(enroll1)
            if u is not None:
                print("U")
                vercode = secrets.token_hex(16)
                user = UserProfile.objects.create_user(email=u.email,fname=u.fname,lname=u.lname,dept=u.dept,enroll=enroll1,password=request.POST['password'],grad_year=u.grad_year,verification_code=vercode)
                print("User")
                # inactive_user = send_verification_email(request, form)
                #user = UserProfile.objects.create_user(email=request.POST['email'],Name=request.POST['name'],Branch=request.POST['branchname'],Enrollment=request.POST['Enroll'],Role=request.POST['groupOfDefaultRadios'],mobile=request.POST['mobile'],password=request.POST['pass'])
                subject = 'Email Verification'
                message = 'Please Verify your email by clicking the link given below http://127.0.0.1:8000/emailverification/' + vercode
                recepient = str(u.email)
                print(recepient)
                send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
                print("Sent")

                return render(request,template_name='signup.html',context = {'x':0})

                return jsonify({"success": True})
            else:
                return jsonify({"success": False})
            print(5)

        except:
            # return HttpResponse("Please Check Enrollment Number")
            return render(request, 'signup.html',context = {'x':1})

def emailverification(request, ver):
    u = UserProfile.objects.get(verification_code=ver)
    u.is_Email_Verified = True
    u.save()
    return render(request, 'emailverification.html', context = {'u':u})


# Check if valid enrollment number
def validate_username(request):
    print("YES")
    enroll = request.GET.get('enroll', None)
    data = {
        'is_taken': CollegeData.objects.filter(enroll__iexact=enroll).exists(),
        'is_taken1': UserProfile.objects.filter(enroll__iexact=enroll).exists()
    }
    # return JsonResponse(data)
    if data['is_taken1']:
        data['error_message'] = 'User Already Exixts.'
    elif data['is_taken']:
        data['error_message'] = 'Invalid Enrollment Number.'
    return JsonResponse(data)


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        user = auth.authenticate(request, email = email, password = password)
        x = user.is_Email_Verified

        if user is not None and x:
            print(user)
            auth.login(request,user)
            u = UserProfile.objects.get(email = email)
            # myfile = request.FILES['picture']
            # fs = FileSystemStorage()
            # filename = fs.save(myfile.name, myfile)
            # uploaded_file_url = fs.url(filename)
            # return render(request, 'userprofile.html', {
            #     'uploaded_file_url': uploaded_file_url
            # })

            return render(request,'userprofile.html')
        else:
            return HttpResponseRedirect(reverse_lazy(login))
    else:
        return render(request,template_name='login.html')


def profile(request):
    if request.method == 'GET':
        return render(request,'userprofile.html')
    if request.method == 'POST':
        myfile = request.FILES['picture']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        request.user.avtar = filename
        request.user.save()

        return HttpResponseRedirect(reverse_lazy(profile))




def contact(request):
    return render(request, 'contactus.html')

def logout(request):
    auth.logout(request)
    return redirect(home)

def faq(request):
    return render(request, 'FAQ.html')

def share(request):
    return render(request,'addnotes.html')

def upload(request):
    if request.method == 'POST':
        myfile = request.FILES['picture']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        try:
            price = request.POST['price']
        except:
            price = 0
        try:
            isbn = request.POST['isbn']
        except:
            isbn = "NA"

        # return render(request, 'addnotes.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })
        book = Resource(Title=request.POST['title'],Category=request.POST['category'],DP=filename,Description=request.POST['desc'],Type=request.POST['optradio'] or "Free",Price=price,Branch=request.POST['branch'],isbn=isbn)
        print(request.user)
        book.user=request.user
        book.save()
        if request.POST['category'] == "Reference book":
            print(11)
            o = newRequest.objects.filter(isbn=request.POST['isbn'])
            for j in o:
                subject = 'Reference Book Uploaded'
                message = 'You have requested for the Reference Book with ISBN: ' + j.isbn + ' which is currently uploaded by ' + request.user.fname + ' ' + request.user.lname
                recepient = str(j.req.email)
                print(recepient)
                send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
                print("Sent")



        return HttpResponseRedirect(reverse_lazy(dashboard))

#for testing purpose only
def display(request):
    a = Resource.objects.all()
    return render(request,'tryy.html',context = {'a':a})

def search(request):
    if request.method == 'GET':
        return render(request,'searchnotes.html')

    if request.method == 'POST':
        q = request.POST['query']
        result = Resource.objects.filter(Title__icontains=q)
        p = request.POST['branch']
        r = request.POST['type']
        c = request.POST['pay']
        if r!="All":
            result = result.filter(Category=r)
        if p!="All":
            result = result.filter(Branch=p)
        if c!="All":
            result = result.filter(Type=c)
        l = len(result)

        return render(request,'searchnotes.html',context = {'r':result,'l':l})

def details(request,id):
    if request.method == "GET":
        b = Resource.objects.get(id=id)
        # rating = None
        # average = None
        # try:
        #     print(1)
        #     # res = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key":"4obs0JcZebFbBlPvF8Gf3g","isbns":b.isbn})
        #     url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn;
        #     # print(res)
        #     result=res.json()
        #     print(result)
        #     rating=result['books'][0]['work_text_reviews_count']
        #     average=result['books'][0]['average_rating']
        # except:
        #     pass
        if request.user.is_authenticated:
            x = requestedResources.objects.filter(req=request.user)
            print(x)
            x = x.filter(res=b)
        else:
            x = None
        return render(request,'notedetails.html',context={'b':b,'x':x})

def details1(request):
    if request.method == "GET":
        dept_id = request.GET.get('book_id', -1)
        b = Resource.objects.get(id=dept_id)
        req = request.user
        r = req.enroll
        don = b.user.enroll
        d = UserProfile.objects.get(enroll=don)
        #Sending send_mail
        subject = 'Request Received'
        message = 'You have received request for the Resource ' + b.Title + ' from ' + req.fname + ' ' + req.lname
        recepient = str(d.email)
        print(recepient)
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        print("Sent")

        ob = requestedResources.objects.create(req=req,don=don,res=b)

        return render(request,'success.html',context={'message':'Your Request has been Succesfully Submited!!...'})

def dashboard(request):
    if request.method == 'GET':
        req = requestedResources.objects.filter(don=request.user.enroll)
        up = Resource.objects.filter(user=request.user)
        return render(request,'buyerrequests.html',context={'r':req,'u':up})

def deletebook(request,id):
    b = Resource.objects.get(id=id)
    b.delete()
    return HttpResponseRedirect(reverse_lazy(dashboard))

def approve(request,id):
    b = requestedResources.objects.get(id=id)
    d = UserProfile.objects.get(enroll=b.don)
    subject = 'Request Approved'
    message = 'Yeehh!! 🥳🥳\n Your request for the Resource ' + b.res.Title + ' is Successfully approved by ' + d.fname + ' ' + d.lname
    message += ' Contact details of donor\n Email: ' + d.email
    recepient = str(b.req.email)
    print(recepient)
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    print("Sent")
    b.delete()
    return HttpResponseRedirect(reverse_lazy(dashboard))

def reject(request,id):
    b = requestedResources.objects.get(id=id)
    d = UserProfile.objects.get(enroll=b.don)
    subject = 'Request Rejected'
    message = 'Oopss!! 😟\n Your request for the Resource ' + b.res.Title + ' is Rejected by ' + d.fname + ' ' + d.lname
    # message += ' Contact details of donor\n Email: ' + d.email
    recepient = str(b.req.email)
    print(recepient)
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    print("Sent")
    b.delete()
    return HttpResponseRedirect(reverse_lazy(dashboard))

def newrequests(request):
    if request.method == "GET":
        r = requestedResources.objects.filter(req=request.user)
        u = newRequest.objects.filter(req=request.user)
        return render(request,"dashboard.html",{'r':r,'u':u})
    if request.method == "POST":
        print(1)
        ob = newRequest.objects.create(req=request.user,isbn=request.POST['isbn'])
        return HttpResponseRedirect(reverse_lazy(newrequests))

def delreq(request,id):
    b = requestedResources.objects.get(id=id)
    b.delete()
    return HttpResponseRedirect(reverse_lazy(newrequests))

def deletenew(request,id):
    b = newRequest.objects.get(id=id)
    b.delete()
    return HttpResponseRedirect(reverse_lazy(newrequests))

def suggest(request):
    x = contactUs.objects.create(name=request.POST['name'],email=request.POST['email'],subject=request.POST['subject'],suggestion=request.POST['cmt'])
    return render(request,"thank.html",{'name':x.name})

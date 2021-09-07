from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,LoginForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .models import *
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime,timedelta

# Create your views here.
def home(request):
    objects = order.objects.all()
    for obj in objects:
        if obj.enddaytime < timezone.now():
            bike.objects.filter(pk=obj.bikeid.id).update(available=True)
    return render(request,'first/home.html')

def about(request):
    return render(request,'first/about.html')

def bikes(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            City = request.POST.get('city')
            start = request.POST.get('stdate')
            end = request.POST.get('enddate')
            request.session['city'] =City
            request.session['start'] = start
            request.session['end'] = end
        b = bike.objects.filter(available=True)
        return render(request,'first/bikes.html',{'bike':b})
    else:
        return render(request,'first/bikeform.html')


def addTocart(request,id):
    if request.user.is_authenticated:
        request.session['bike']=id
        b = bike.objects.get(pk=id)
        return render(request,'first/book.html',{'bike':b})
    else:
        return HttpResponseRedirect('/login/')



def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    request.session['user'] = uname
                    request.session['bike']=0
                    messages.success(request,"Logined successfully!!")
                    login(request,user)
                    return HttpResponseRedirect('/bikes/')
                form.save()
        else:
            form = LoginForm()
        return render(request,'first/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/bikes/')


def user_signup(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"Your account is created successfully!!")
            form.save()
    else:
        form = SignUpForm()
    return render(request,'first/signup.html',{'form':form})

def cart(request):
    if request.user.is_authenticated:
        if request.session['bike'] != 0:
            bid = request.session['bike']
            instance = bike.objects.get(pk=bid)
            userinstance = User.objects.get(pk=request.user.id)
            s = request.session['start']
            e = request.session['end']
            o = order.objects.create(bikeid=instance,userid=userinstance,startdaytime=s,enddaytime=e)
            o.save()
            bike.objects.filter(pk=bid).update(available=False)
            messages.success(request,"ORDER PLACED!!")
            request.session['bike']=0
        orders = order.objects.filter(userid = request.user)
        future_ord = []
        current_ord = []
        past_ord = []
        for ord in orders:
            if ord.enddaytime > timezone.now() and ord.startdaytime > timezone.now():
                future_ord.append(ord)
            elif ord.enddaytime > timezone.now() and ord.startdaytime < timezone.now():
                current_ord.append(ord)
            elif ord.enddaytime < timezone.now() and ord.startdaytime < timezone.now():
                past_ord.append(ord)
        return render(request,'first/cart.html',{'future':future_ord,'current':current_ord,'past':past_ord})

def order_detail(request,id):
    obj = order.objects.get(pk=id)
    userinst = User.objects.get(pk=obj.userid.id)
    Endday = obj.enddaytime
    Startday = obj.startdaytime
    Eday = Endday.strftime("%d")
    Emonth = Endday.strftime("%m")
    Eyear = Endday.strftime("%Y")
    Sday  = Startday.strftime("%d")
    Smonth = Startday.strftime("%m")
    Syear = Startday.strftime("%Y")
    Ehour = Endday.strftime("%H")
    Eminute = Endday.strftime("%M")
    Esecond = Endday.strftime("%S")
    Shour = Startday.strftime("%H")
    Sminute = Startday.strftime("%M")
    Ssecond = Startday.strftime("%S")
    yeardiff = round((int(Eyear) - int(Syear))*365,1)
    monthdiff = round((int(Emonth) - int(Smonth))*30,1)
    daydiff = (int(Eday) - int(Sday))
    hourdiff = round((int(Ehour) - int(Shour))/24,1)
    minutediff = round((int(Eminute) - int(Sminute))/(24*60),1)
    seconddiff = round((int(Esecond) - int(Ssecond))/(24*60*60),1)
    rent = (yeardiff+daydiff+monthdiff+hourdiff+minutediff+seconddiff)*(obj.bikeid.costperday)  
    return render(request,"first/orderdetail.html",{'order':obj,'user':userinst,'rent':rent})


def cancel_order(request,id):
    obj = order.objects.get(pk=id)
    bike.objects.filter(pk=obj.bikeid.id).update(available=True)
    obj.delete()
    messages.success(request,"Order successfully cancelled!!")
    return HttpResponseRedirect('/cart/')

def profile(request):
    object = User.objects.get(pk=request.user.id)
    return render(request,'first/profile.html',{'user':object})

def user_logout(request):
    if 'user' in request.session:
        del request.session['user']
    if 'bike' in request.session:
        del request.session['bike']
    if 'city' in request.session:
        del request.session['city']
    if 'start' in request.session:
        del request.session['start']
    if 'end' in request.session:
        del request.session['end']
    logout(request)
    return HttpResponseRedirect('/')

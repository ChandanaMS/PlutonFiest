from django.shortcuts import render
from .forms import UserForm,UserProfileInforForm,PaymentForm,EventRegisterationsForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from backend.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail

# Create your views here.

def index(request):
    return render(request,'pluton/index.html')

def home(request):
    return render(request,'pluton/home.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('pluton:index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInforForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInforForm()
    return render(request,'pluton/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                email=user.email
                subject = 'Welcome'
                message = 'Thank you! U have successfully logged in to the site'
                recepient =str(email)
                send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
                return HttpResponseRedirect(reverse('pluton:home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'pluton/login.html', {})
'''
def subscribe(request):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        subject = 'Welcome'
        message = 'Thank you! U have successfully subscribed to the site'
        recepient = str(sub['Email'].value())
        send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'pluton/success.html', {'recepient': recepient})
    return render(request, 'pluton/index1.html', {'form':sub})
'''

def payment(request):
    paid=False
    if request.method == 'POST':
        payment_form=PaymentForm(data=request.POST)
        if payment_form.is_valid():
            #payment = payment_form.save(commit=False)
            #payment.save()
            paid=True
            print("Payment successful")
            return HttpResponseRedirect(reverse('pluton:succ'))

        else:
            print("Payment failed")
            print(payment_form.errors)
    else:
        payment_form = PaymentForm()
    return render(request,'pluton/payment.html',
                          {'payment_form':payment_form,
                           'paid':paid})

def chatbot(request):
    return render(request,'pluton/chatbot.html')

def succ(request):
    return render(request,'pluton/succ.html')

def culturals(request):
    return render(request,'pluton/culturals.html')
def scitech(request):
    return render(request,'pluton/scitech.html')
def sports(request):
    return render(request,'pluton/sports.html')
def artlit(request):
    return render(request,'pluton/artlit.html')

def streetplay(request):
    return render(request,'pluton/streetplay.html')
def westernband(request):
    return render(request,'pluton/westernband.html')
def photography(request):
    return render(request,'pluton/photography.html')
def hackathon(request):
    return render(request,'pluton/hackathon.html')
def sciencequiz(request):
    return render(request,'pluton/sciencequiz.html')
def chess(request):
    return render(request,'pluton/chess.html')
def ctf(request):
    return render(request,'pluton/ctf.html')
def basketball(request):
    return render(request,'pluton/basketball.html')
def themepaint(request):
    return render(request,'pluton/themepaint.html')
def creativewriting(request):
    return render(request,'pluton/creativewriting.html')

def registerevent1(request):
    registered1=False
    amount=0
    if request.method == 'POST':
        regevent_form=EventRegisterationsForm(data=request.POST)
        if regevent_form.is_valid():
            registered = regevent_form.save()
            registered.save()
            registered1=True
            if registered.event=='Culturals':
                amount=200
            elif registered.event=='Sci_tech':
                amount=300
            elif registered.event=='Sports':
                amount=150
            else:
                amount=250
            
            print("Registeration successful. Proceed to payment")
            #return render(request, 'pluton/payment.html', {'amount': amount})
            return HttpResponseRedirect(reverse('pluton:payment'))
            

        else:
            print("Event Registeration failed")
            print(regevent_form.errors)
    else:
        regevent_form = EventRegisterationsForm()
    return render(request,'pluton/registerevent1.html',
                          {'regevent_form':regevent_form ,
                           'amount':amount,
                           'registered1':registered1})
    

#def payment(request):
 #   return render(request,'pluton/payment.html')



def about(request):
    return render(request,'pluton/about.html')
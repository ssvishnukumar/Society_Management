from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model  # with the help of this we can authenticate the users and then we can allow them to proceed further.
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView
from user_login.forms import RegistrationForm, LoginForm, NewsForm, ComplaintForm
from user_login.forms import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
import random
from django.conf import settings
from .models import Account, News, BuyRent, Visitors


@login_required(login_url='/user_login/login/')
def newsadd(request):
    form = NewsForm()
    if request.method=='POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user_login/user_dashboard/')
    context={
        'form':form,
    }
    return render(request,'post/news_add.html',context)
    # render responds by HTTP response of context. Here (i.e) forms

def visitors_add(request):
    form = VisitorsForm()
    if request.method=='POST':
        form = VisitorsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user_login/user_dashboard/')
    context = {
        'form':form,
    }
    return render(request,'visitors_add.html',context)
        
        
def complaint_add(request):
    form = ComplaintForm()
    if request.method=='POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            # here by default it will choose Complaint in models...because we have given that default as 0. (i.e) Complaint
            form.save()
            return redirect('/user_login/user_dashboard/')
        
    context = {
        'complaints':form,
    }
    return render(request,'complaint_add.html',context)

def suggestion_add(request):
    form = SuggestionForm()
    if request.method == 'POST':
        a = ComplaintSuggestion.objects.create()
        a.email = request.POST['email']
        a.name = request.POST['name']
        a.title = request.POST['title']
        a.content = request.POST['content']
        a.choose = 1
        a.save()
        return redirect('user_login:user_dashboard')
    context = {
        'suggestions':form,
    }
    return render(request,'suggestion_add.html',context)
       
# class NewsList(ListView):
#     queryset = News.objects.filter(status=1).order_by('-created_on')
#     template_name = 'user_login:dashboard.html'
    
#     def get_absolute_url(self):
#         context = {
#             'pk': self.id,
            
#         }
    

# class NewsDetail(DetailView):
#     model = News
#     template_name = 'user_login:news_detail.html'
#     def get_absolute_url(self):
#         context = {
#             'pk': self.id,
            
#         }
    
    
# class NewsDelete(DeleteView):
#     model = News
#     template_name = 'user_login:news_delete.html'
#     success_url = reverse_lazy('user_login:dashboard')# it asked to provide a success url, so...

def dashboard_view(request):
    obj = News.objects.filter(status=1).order_by('-created_on')[:10]
    return render(request,'dashboard.html', {'news': obj})
        

def user_dashboard_view(request):
    obj = News.objects.filter(status=1).order_by('-created_on')[:10]
    visitor = Visitors.objects.filter().order_by('-date_joined')[:4]
    return render(request,'user_dashboard.html', {'news': obj, 'visitor':visitor})
    
def buyview(request):
    form = BuyForm()
    if request.POST:
        buy = BuyRent.objects.create()
        buy.email = request.POST['email']
        buy.username = request.POST['username']
        buy.first_name = request.POST['first_name']
        buy.last_name = request.POST['last_name']
        buy.mobile_no = request.POST['mobile_no']
        buy.flat_type = request.POST['flat_type']
        # buy.cleaning_house = request.POST['cleaning_house']
        buy.furnished = request.POST['furnished']
        buy.buy_flat = True
        # pdb.set_trace()
        buy.save()
        return redirect('user_login:thanks')
    context= {
        'buy':form
    }
    return render(request, 'buyflat.html', context)

def rentview(request):
    form = RentForm()
    if request.POST:
        rent = BuyRent.objects.create()
        rent.email = request.POST['email']
        rent.username = request.POST['username']
        rent.first_name = request.POST['first_name']
        rent.last_name = request.POST['last_name']
        rent.mobile_no = request.POST['mobile_no']
        rent.flat_type = request.POST['flat_type']
        
        #Use the MultiValueDict's get method. This is also present on standard dicts and is a way to fetch a value while providing a default if it does not exist.
        rent.pool = request.POST.get('pool')
        rent.gym = request.POST.get('gym')
        rent.creche = request.POST.get('creche')
        rent.cleaning_house = request.POST.get('cleaning_house')
        
        if rent.pool == 'on':
            rent.pool = True
        else:
            rent.pool = False
            
        if rent.gym == 'on':
            rent.gym = True 
        else:
            rent.gym = False
            
        if rent.creche == 'on':
            rent.creche = True 
        else:
            rent.creche = False
            
        if rent.cleaning_house == 'on':
            rent.cleaning_house = True
        else:
            rent.cleaning_house = False
            
        rent.furnished = request.POST['furnished']
        rent.no_of_members = request.POST['no_of_members']
        rent.rent_flat = True
        rent.save()
        return redirect('user_login:thanks')
    context = {
        'rent': form
    }
    return render(request, 'rentflat.html', context)

def thanksview(request):
    return render(request, 'thanks.html')

def resident_view(request):
    usr = Account.objects.filter().order_by('-date_joined')
    return render(request, 'resident.html', {'resident':usr})

        
def registration_view(request):
    context = {}
    form = RegistrationForm(request.POST)
    context['registration_form'] = form
    # print(request.method == "POST")
    try:
        if request.method == "POST":
            email = request.POST['email']
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            flat_no = request.POST['flat_no']
            mobile_no = request.POST['mobile_no']
            tower_no = request.POST['tower_no']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 != password2:
                form = RegistrationForm(request.POST)
                context['registration_form'] = form
                return render(request, 'register.html',context)
            # if Account.objects.filter(email=email).first():
            #     messages.success(request, 'Email is taken')
            #     return redirect('/user_login/register/')
                # messages.error(request, 'password does not match')
                # return redirect('user_login:register')

            user = Account.objects.create_user(email, username, password=password1)
            user.first_name = first_name
            user.last_name = last_name
            user.flat_no = flat_no
            user.tower_no = tower_no
            user.mobile_no = mobile_no

            user.save()
            
            # print(user)
            user_otp= random.randint(1000,9999)

            request.session['email'] = email 
            request.session['otp'] = user_otp
 
            mess= f"Hello {user.email}, \n Your OTP is {user_otp} \n Thank You"

            # print(user_otp)

            send_mail(
                  "OTP for Registration.",
                    mess,
                   settings.EMAIL_HOST_USER,
                   [user.email],
                   fail_silently= False
                    )

            return redirect('user_login:otp')
        else: # GET
            form = RegistrationForm()
            context['registration_form'] = form
    except IntegrityError:
        err = email + ' already exist'
        messages.error(request, err)
    return render(request, "register.html", context)


def login_view(request):
    context = {}
    # user = request.user

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            
            user = authenticate(email=email, password=password)
            if user:
                # here wer are allowing the user to login.
                login(request,user)
                return redirect('user_login:user_dashboard')
                # return render(request, 'dashboard.html')
    # if user.is_authenticated:  # if the user is authenticated we are redirecting ..
    #     # messages.success(request, 'You are already authenticated user.')
    #     return redirect('user_login:dashboard')

    else: 
        # here the user is still not attempted to login. (i.e) GET
        form = LoginForm()
    context['login_form'] = form
    return render(request, 'login.html', context)


def logout_view(request):
    # user = (request, user)
    # user.is_active = False
    logout(request)
    return redirect('user_login:dashboard')


def otp_view(request):
    # OTP = send_otp(request.session['email'])
    OTP = request.session['otp']
    if request.method == "POST":

        # po = Status.objects.latest('id')
        # email = request.session['email']
        # pdb.set_trace()
        if OTP == int(request.POST['otp']):
            user = Account.objects.get(email=request.session['email'])
            # usr = Account.objects.all()
            user.is_verified = True
            # pdb.set_trace()
            user.save()

            # usr.save()
            return redirect('user_login:login')
        else:
            messages.error(request, "OTP does not match. recheck or click to resend otp")
        return render(request, 'otp.html', {'error':{"Password doesn't match"}})
    return render(request, 'otp.html')




import pdb
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model  # with the help of this we can authenticate the users and then we can allow them to proceed further.
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView
from user_login.forms import RegistrationForm, LoginForm, NewsForm, ComplaintForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
import random
from django.conf import settings
from .models import Account, News
# Account = get_user_model()

@login_required(login_url='/user_login/login/')
def newsadd(request):
    form = NewsForm()
    if request.method=='POST':
        form = NewsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/user_login/dashboard/')
    context={
        'form':form,
    }
    return render(request,'news_add.html/',context)
    # render responds by HTTP response of context. Here (i.e) forms

class NewsList(ListView):
    queryset = News.objects.filter(status=1).order_by('-created_on')
    template_name = 'user_login:dashboard.html'

class NewsDetail(DetailView):
    model = News
    template_name = 'user_login:news_detail.html'
    
class NewsDelete(DeleteView):
    model = News
    template_name = 'user_login:news_delete.html'
    success_url = reverse_lazy('user_login:dashboard')# it asked to provide a success url, so...


    
@login_required(login_url='/user_login/login/')
def complaintadd(request):
    form= ComplaintForm()
    if request.method=='POST':
        form= ComplaintForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/user_login/dashboard/')
    context={
        'form':form,
    }
    return render(request,'post/complaint_add.html',context)
    # render responds by HTTP response of context. Here (i.e) forms
    
    
def registration_view(request):
    context = {}
    form = RegistrationForm(request.POST)
    context['registration_form'] = form
    # print(request.method == "POST")
    try:
        if request.method == "POST":
            # email = request.POST['email']
            # phone = request.POST['mobile_no']
            # flat = request.POST['flat_no']
            # tower = request.POST['tower_no']
            # password1 = request.POST['password1']
            # password2 = request.POST['password2']
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
        else:
            form = RegistrationForm()
            context['registration_form'] = form
    except IntegrityError:
        err = email + ' already exist'
        messages.error(request, err)
    return render(request, "register.html", context)


def login_view(request):
    context = {}
    user = request.user

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
            # pdb.set_trace()
            user.save()

            # usr.save()
            return redirect('user_login:login')
        else:
            messages.error(request, "OTP does not match. recheck or click to resend otp")
            return render(request, 'otp.html', {'error':{"Password doesn't match"}})
    return render(request, 'otp.html')


def dashboard_view(request):
    return render(request,'dashboard.html')

def user_dashboard_view(request):
    return render(request,'user_dashboard.html')




















































# def registration_view(request):
#     context ={}
#     if request.POST:
#         form = RegistrationForm(request.POST)
#         if form.is_valid(): # if the user enter every required field, and everything is correctit allows us to proceed further...
#             form.save() # if the form is valid, then here we are saving.
#             email = form.cleaned_data.get('email') # this is the way we get the data from a valid form...
#             raw_password = form.cleaned_data.get('password1')
#             account = authenticate(email=email, password=raw_password)
#
#             # here, after authenticating the user and creating the user object ...now we have the user object...
#             # now we can call the login
#             login(request, account)
#             return redirect('dashboard') # here it will redirect to the dashboard name in urls...if its there ....else it will show error ...
#
#         # if the form is not valid,
#         else:
#             context['registration_form'] = form # here the registration form is the name that we have created for the context.
#     # here if the request isnot the POST request, then its the GET request...
#     # that means that they are visiting the registration_view for the first time...
#     else: # GET request ................
#         # this means, they still not attempted to click register
#         form = RegistrationForm()
#         context['registration_form'] = form
#     return render(request, 'register.html', context)
# #When you use a Django Template, it is compiled once (and only once) and stored for future use, as an optimization. A template can have variable names in double curly braces, such as {{ myvar1 }} and {{ myvar2 }}.
# #A Context is a dictionary with variable names as the key and their values as the value. Hence, if your context for the above template looks like: {myvar1: 101, myvar2: 102}, when you pass this context to the template render method, {{ myvar1 }} would be replaced with 101 and {{ myvar2 }} with 102 in your template. This is a simplistic example, but really a Context object is the context in which the template is being rendered.



# def otp_view(request):
#     if request.method == "POST":
#         get_otp = request.POST.get('otp')
#         # if get_otp:
#         #     get_user = request.POST.get('user')
#         #     usr = User.objects.get(username=get_user)
#         #     if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
#         #         return render(request, "login.html")
#         #pdb.set_trace()
#         for key, value in request.session.items():
#             print(key)
#         usr = Account.objects.get(email=request.session['email'])
#         print(usr)
#         user = UserOTP.objects.get(usr)
#         if user.user_otp == get_otp:
#             # user=User.objects.get(email=request.POST['email'])
#             # user.save()
#             return redirect('user_login:login')
#         else:
#             messages.error(request, f'You entered the wrong OTP')
#     return render(request,'otp.html')


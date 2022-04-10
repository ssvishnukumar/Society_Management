from django.contrib.auth import login, logout, authenticate, get_user_model  # with the help of this we can authenticate the users and then we can allow them to proceed further.
from user_login.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import UserOTP
from django.core.mail import send_mail
from django.contrib import messages
import random
from django.conf import settings

Account = get_user_model()

def registration_view(request):
    context = {}
    form = RegistrationForm(request.POST)
    print(request.method == "POST")
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['mobile_no']
        flat = request.POST['flat_no']
        tower = request.POST['tower_no']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html', {'error': "Password does not match"})


        user = Account.objects.create_user(email, password1)
        user.flat = flat
        user.tower = tower
        user.phone = phone
        user.email = email
        user_otp= random.randint(1000,9999)
        user.save()
        print(user,user_otp)
        UserOTP.objects.create(user=user,otp=user_otp)


        mess= f"Hello {user.email}, \n Your OTP is {user_otp} \n Thank You"

        print(user_otp)
        send_mail(
              "Welcome",
               mess,
               settings.EMAIL_HOST_USER,
               [user.email],
               fail_silently= False
                )
        request.session['email']=email
        print(email)
        return redirect('user_login:otp')

    context['registration_form'] = form
    return render(request, "register.html", context)


#
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
#


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
                return redirect('user_login:dashboard')
    if user.is_authenticated:  # if the user is authenticated we are redirecting ..
        # messages.success(request, 'You are already authenticated user.')
        return redirect('user_login:dashboard')

    else:
        # here the user is still not attempted to login. (i.e) GET
        form = LoginForm()
    context['login_form'] = form
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('user_login:dashboard')


def otp_view(request):
    if request.method == "POST":
        get_otp = request.POST.get('otp')
        # if get_otp:
        #     get_user = request.POST.get('user')
        #     usr = User.objects.get(username=get_user)
        #     if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
        #         return render(request, "login.html")
        #pdb.set_trace()
        for key, value in request.session.items():
            print(key)
        usr = Account.objects.get(email=request.session['email'])
        print(usr)
        user = UserOTP.objects.get(usr)
        if user.user_otp == get_otp:
            # user=User.objects.get(email=request.POST['email'])
            # user.save()
            return redirect('user_login:login')
        else:
            messages.error(request, f'You entered the wrong OTP')
    return render(request,'otp.html')

def dashboard_view(request):
    return render(request,'dashboard.html')



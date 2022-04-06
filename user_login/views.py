from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate # with the help of this we can authenticate the users and then we can allow them to proceed further.
from user_login.forms import RegistrationForm

from django.contrib.auth import login
from django.urls import reverse_lazy  # for redirecting back


def registration_view(request):
    context ={}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid(): # if the user enter every required field, and everything is correctit allows us to proceed further...
            form.save() # if the form is valid, then here we are saving.
            email = form.cleaned_data.get('email') # this is the way we get the data from a valid form...
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)

            # here, after authenticating the user and creating the user object ...now we have the user object...
            # now we can call the login
            login(request, account)
            return redirect('dashboard')
        # if the form is not valid,
        else:
            context['registration_form'] = form
    # here if the request isnot the POST request, then its the GET request...
    # that means that they are visiting the registration_view for the first time...
    else: # GET request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)
#When you use a Django Template, it is compiled once (and only once) and stored for future use, as an optimization. A template can have variable names in double curly braces, such as {{ myvar1 }} and {{ myvar2 }}.
#A Context is a dictionary with variable names as the key and their values as the value. Hence, if your context for the above template looks like: {myvar1: 101, myvar2: 102}, when you pass this context to the template render method, {{ myvar1 }} would be replaced with 101 and {{ myvar2 }} with 102 in your template. This is a simplistic example, but really a Context object is the context in which the template is being rendered.














#
# class UserRegisterView(generic.CreateView):
#     form_class = RegisterForm # default creation form in django for
#     template_name = 'register.html'
#     success_url = reverse_lazy('/') # it generates the url
#
# def register(request):
#     # if request.method == 'GET':
#     #     form = RegisterForm()
#     #     context ={
#     #         'form': form
#     #     }
#     #     return render(request, 'register.html', context=context)
#
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Registration successful.")
#             return redirect("")
#         messages.error(request, "Unsuccessful user_login. Invalid information.")
#     form = UserCreationForm()
#     return render(request=request, template_name="register.html", context={"register_form": form})
#

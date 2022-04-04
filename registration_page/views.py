from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy  # for redirecting back


class UserRegisterView(generic.CreateView):
    form_class = UserCreationForm # default creation form in django for
    template_name = 'register.html'
    success_url = reverse_lazy('registration_page') # it generates the url

# def register_request(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Registration successful.")
#             return redirect("")
#         messages.error(request, "Unsuccessful registration. Invalid information.")
#     form = UserCreationForm()
#     return render(request=request, template_name="register.html", context={"register_form": form})
#

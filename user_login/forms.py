from django.contrib.auth.forms import UserCreationForm
from django import forms
from user_login.models import Account
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    email= forms.EmailField(max_length=50, help_text='Enter a valid EMAIL of yours!')
    mobile_no = forms.IntegerField(max_value=10000000000, )
    flat_no = forms.IntegerField(max_value=10000, )
    tower_no = forms.IntegerField(max_value=10000, )

    #https://www.youtube.com/watch?v=oZUb372g6Do&list=PLgCYzUzKIBE_dil025VAJnDjNZHHHR9mW&index=14&ab_channel=CodingWithMitch
    # watch at 2.10 min to know more about class Meta

    # here we are gonna tell registration form that.. what the form needs to look like.
    class Meta:
        model = Account
        fields = ('email', 'username','first_name', 'last_name','mobile_no','tower_no','flat_no', 'password1', 'password2', )



class LoginForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput) # PasswordInput hides the the password input

    class Meta:
        model = Account
        fields = ('email', 'password',)

    def clean(self): # here self is form
        if self.is_valid():
            # this clean method runs before anything in the forms
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password): # here if anything in this email and password entered is wrong..then it will raise the error
                raise forms.ValidationError("Invalid Data")






# from .models import Profile
#
# class RegisterForm(UserCreationForm):
#     email= forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email'}))
#     # username= forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
#     mobile_no= forms.IntegerField(max_value=10000000000, required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Mobile No.'}))
#     flat_no= forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Flat No.'}))
#     tower_no= forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Tower No.'}))
#     # password1= forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create Password'}))
#     # password2= forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Password Again.'}))
#
#     class Meta:
#         model = User
#         fields = ('email','username', 'mobile_no', 'flat_no', 'tower_no', 'password1','password2')
#
#     def __init__(self, *args, **kwargs):
#         super(RegisterForm, self).__init__(*args, **kwargs)
#
#         self.fields['username'].widget.attrs['class']='form-control'
#         self.fields['password1'].widget.attrs['class']='form-control'
#         self.fields['password2'].widget.attrs['class']='form-control'

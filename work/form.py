from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email",widget=forms.TextInput(attrs={'class':'form-control','required':'true','placeholder':'Email'}))
    sex = forms.ChoiceField(widget=forms.Select(attrs={'class': 'sex', 'required': 'true', 'placeholder': 'Sex', }),
                            choices=sex_choices, )

    year = forms.ChoiceField(widget=forms.Select(attrs={'class': 'year', 'required': 'true', 'placeholder': 'Year', }),
                             choices=year_choices, )

    class Meta:
        model = User
        fields = ['username','email','sex','year','password1','password2']

class ContactForm(forms.ModelForm):

    class Meta:
        model = contact
        fields = ['name','email','number','message']
from django import forms
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=100, required=False, help_text='Optional')
	last_name = forms.CharField(max_length=100, required=False, help_text='Optional')
	email = forms.EmailField(max_length=500, help_text='Required. Inform a valid email address')

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'password1','password2']
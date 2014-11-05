from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from . import templater
from django.conf import settings
import decimal, datetime

def process_request(request):
	'''py that handles the ability to add new credit card information to the user's profile'''


	form = UserForm(initial ={
		'email': user.email,
		'first_name': user.first_name,
		'last_name': user.last_name,
		'street': user.street,
		'city': user.city,
		'state': user.state,
		'zipcode': user.zipcode,
		'phone': user.phone,
		'password': user.password,
		'is_staff': user.is_staff,
		'is_superuser': user.is_superuser,
		})
	
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'user_details.html', tvars)

class UserForm(forms.Form):
	card_number = forms.CharField(required=False, label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(required=False, label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	street = forms.CharField(required=False, label='Street', widget=forms.TextInput(attrs={'class':'form-control'}))
	city  = forms.CharField(required=False, label='City', widget=forms.TextInput(attrs={'class':'form-control'}))
	state  = forms.CharField(required=False, label='State', widget=forms.TextInput(attrs={'class':'form-control'}))
	zipcode  = forms.CharField(required=False, label='Zipcode', widget=forms.TextInput(attrs={'class':'form-control'}))
	phone  = forms.CharField(required=False, label='Phone', widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	is_staff = forms.NullBooleanField(required=False, label='Manager', widget=forms.NullBooleanSelect(attrs={'class':'form-control'}))
	is_superuser = forms.NullBooleanField(required=False, label='Admin', widget=forms.NullBooleanSelect(attrs={'class':'form-control'}))
	#def clean_user_text(self):
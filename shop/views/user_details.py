from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from shop import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

def process_request(request):
	'''this py handles to editing of the user's personal information'''
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_superuser == False:
		return HttpResponseRedirect('/manager/')

	'''Shows the list of users'''
	if request.urlparams[0] == "new":
		user = pmod.User()
		user.email = ""
		user.first_name = ""
		user.username = ""
		user.last_name = ""
		user.street = ""
		user.city = ""
		user.state = ""
		user.zipcode = ""
		user.phone = ""
		user.password = ""
		user.is_staff = False
		user.is_superuser = False
		user.is_active = True
	else:
		user = pmod.User.objects.get(id=request.urlparams[0])

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
	
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user.email = form.cleaned_data['email']
			user.username = form.cleaned_data['email']
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.street = form.cleaned_data['street']
			user.city = form.cleaned_data['city']
			user.state = form.cleaned_data['state']
			user.zipcode = form.cleaned_data['zipcode']
			user.phone = form.cleaned_data['phone']
			user.set_password(form.cleaned_data['password'])
			user.is_staff = form.cleaned_data['is_staff']
			user.is_superuse = form.cleaned_data['is_superuser']
			user.is_active = True
			user.save()
			return HttpResponseRedirect('/manager/users')
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'user_details.html', tvars)

class UserForm(forms.Form):
	email = forms.EmailField(required=False, label='Email', widget=forms.TextInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(required=False, label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
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
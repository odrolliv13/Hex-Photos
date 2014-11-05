from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

def process_request(request):
	'''this py handles the login process using a modal'''
	form = LoginForm()

	#when user submits form, this if statement, gets the username and password entered and authenticates the user
	#if authenticated, it logs the user in
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
			if user is not None:
				if user.is_active == True:
					login(request, user)
					redirect = request.META.get("HTTP_REFERER")
					return HttpResponse('<script> window.location.href="' + redirect +'" </script>')
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'loginmodal.html', tvars)

class LoginForm(forms.Form):
	username = forms.CharField(required=False, label='Username', widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

	#function that raises errors if the account has been canceled or if the password does not match
	def clean(self):
		user = authenticate(username = self.cleaned_data.get('username'), password = self.cleaned_data.get('password'))
		if user == None:
			raise forms.ValidationError("The username and password provided do not match")
		if not user.is_active:
			raise forms.ValidationError("This account has been disabled.")
		return self.cleaned_data
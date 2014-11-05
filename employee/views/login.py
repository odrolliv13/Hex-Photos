from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view will log a user in

def process_request(request):
	form = LoginForm()

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
			if user is not None:
				if user.is_active == True:
					login(request, user)
					if request.urlparams[0]:
						redirect = '/employee/' + request.urlparams[0]
						return HttpResponseRedirect(redirect)
					return HttpResponseRedirect('/employee/')
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'login.html', tvars)

class LoginForm(forms.Form):
	username = forms.CharField(required=False, label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

	def clean(self):
		user = authenticate(username = self.cleaned_data.get('username'), password = self.cleaned_data.get('password'))
		if user == None:
			raise forms.ValidationError("The username and password provided do not match")
		if not user.is_active:
			raise forms.ValidationError("This account has been disabled.")
		return self.cleaned_data
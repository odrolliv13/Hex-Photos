from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime
from ldap3 import *

def process_request(request):
	form = LoginForm()

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			s = Server('128.187.61.52', port = 636, get_info = GET_ALL_INFO)
			try:
				c = Connection(s, auto_bind = True, client_strategy = STRATEGY_SYNC, user=form.cleaned_data['username'] + '@intex22.local', password=form.cleaned_data['password'], authentication=AUTH_SIMPLE)
				user = pmod.User.objects.get(username=form.cleaned_data['username'])
				user.set_password(form.cleaned_data['password'])
				user.save()
				user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
				login(request, user)
				return HttpResponseRedirect('/manager')
			except:
				return HttpResponseRedirect('/shop/')
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'login.html', tvars)

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
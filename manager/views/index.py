from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime
from django.contrib.auth import logout

# This view redirects non logged in users to login

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	tvars = {
	
	}	

	return templater.render_to_response(request, 'index.html', tvars)		
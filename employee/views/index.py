from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from manager import models as pmod
from . import templater

# This view checks if user is staff before displaying the employee options

def process_request(request):
	if request.user.is_staff == False:
		return HttpResponseRedirect('/shop/')
		
	tvars = {

	}
	return templater.render_to_response(request, 'index.html', tvars)
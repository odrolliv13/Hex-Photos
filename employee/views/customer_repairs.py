from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.core.mail import send_mail

# This view will return all the repairs for a given user

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shop')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/shop/')
	

	'''Shows the list of catalog_products'''
	if request.urlparams[0]:
		user = pmod.User.objects.get(id = request.urlparams[0])
		Objects = pmod.Repair.objects.filter(paid=False, user = user)

	tvars = {
		'Objects': Objects,
	}
	return templater.render_to_response(request, 'customer_repairs.html', tvars)
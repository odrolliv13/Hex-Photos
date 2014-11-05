from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater

# This view grabs all the transactions that have been received where packed is false

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/')
	
	'''Shows the list of catalog_products'''

	Objects = pmod.Transaction.objects.filter(packed=False)

	tvars = {
		'Objects': Objects,
	}
	return templater.render_to_response(request, 'online_orders.html', tvars)
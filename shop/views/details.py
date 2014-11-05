from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

def process_request(request):
	if "r" in request.urlparams[0]:
		rental = True
		specialid = request.urlparams[0][1:]
	else:
		rental = False
		specialid = request.urlparams[0]

	product = pmod.CatalogProduct.objects.get(id=specialid)

	serialized = pmod.SerializedProduct.objects.filter(catalogID = product, is_active=True, is_rental=False, is_available=True, is_new=True)
	stocked = pmod.StockedProduct.objects.filter(catalogID = product, is_active=True)

	quantity = 0
	if rental == False:
		for i in serialized:
			quantity +=1

		for i in stocked:
			quantity += i.amount

	tvars = {
		'quantity': quantity,
		'rental': rental,
		'product': product,
		
	}
	return templater.render_to_response(request, 'details.html', tvars)
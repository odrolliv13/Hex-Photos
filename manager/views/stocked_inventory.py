from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater

# This view displays the stocked inventory

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/')
	
	'''Shows the list of catalog_products'''
	if request.urlparams[0] == "deleted":
		Objects = pmod.StockedProduct.objects.exclude(is_active=True)
		Object = pmod.StockedProduct()
		ObjectID = 0
		Deleted = True
	elif request.urlparams[0] == "delete":
		catalog_products = pmod.StockedProduct.objects.get(id=request.urlparams[1])
		catalog_products.is_active = False
		catalog_products.save()
		return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

	else:
		Objects = pmod.StockedProduct.objects.exclude(is_active=False)
		Object = pmod.StockedProduct()
		ObjectID = 0
		Deleted = False

	tvars = {
		'Objects': Objects,
		'Object': Object,
		'ObjectID': ObjectID,
		"Deleted": Deleted
	}
	return templater.render_to_response(request, 'stocked_inventory.html', tvars)
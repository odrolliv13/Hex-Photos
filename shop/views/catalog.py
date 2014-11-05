from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from manager import models as pmod
from . import templater

def process_request(request):
	
	if request.urlparams[0]:
		coun = 0
		if request.urlparams[0] == "rentals":
			Category = pmod.Category.objects.get(queryURL = request.urlparams[0])
			possiblerentals = pmod.SerializedProduct.objects.filter(is_rental=True)
			catalogproducts = {}
			for e in possiblerentals:
				catalogproducts[e.catalogID] = 0
			Objects = catalogproducts
			count = 0
			for o in Objects:
				count += 1
			if count < 1:
				results = False
			else:
				results = True
			allcatalog = False
			rental = True

		else:
			Category = pmod.Category.objects.get(queryURL = request.urlparams[0])
			Objects = pmod.CatalogProduct.objects.filter(category=Category, is_active=True)
			count = 0
			for o in Objects:
				count += 1
			if count < 1:
				results = False
			else:
				results = True
			allcatalog = False
			rental = False

	else:
		Objects = pmod.Category.objects.filter(is_active=True)
		allcatalog = True
		results = True
		rental = False
	
	tvars = {
		'Objects': Objects,
		'allcatalog': allcatalog,
		'results': results,
		'Category': Category, 
		'rental': rental,
		'coun' : coun,
	}
	return templater.render_to_response(request, 'catalog.html', tvars)
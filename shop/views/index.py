from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from manager import models as pmod
from . import templater

def process_request(request):
	p11 = pmod.CatalogProduct.objects.get(id = 11)
	p9 = pmod.CatalogProduct.objects.get(id = 9)
	p3 = pmod.CatalogProduct.objects.get(id = 3)

		
	tvars = {
		'p11': p11,
		'p9': p9,
		'p3': p3,
			
	}
	return templater.render_to_response(request, 'index.html', tvars)
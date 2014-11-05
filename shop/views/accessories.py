from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from manager import models as pmod
from . import templater

def process_request(request):
	Category = pmod.Category.objects.get(name="Accessories")
	Objects = pmod.CatalogProduct.objects.filter(category=Category, is_active=True)
	Object = pmod.CatalogProduct()
	
	tvars = {
		'Objects': Objects,
		'Object': Object,
	}
	return templater.render_to_response(request, 'accessories.html', tvars)
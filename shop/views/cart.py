from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from manager import models as pmod
from . import templater

def process_request(request):
	'''py that handles the cart. It creates a new dictionary with each session '''
	cart = request.session.get('cart', {})
	Objects = {}
	
	if request.urlparams[0] == "remove":
		if request.urlparams[1] in cart:
			if cart[request.urlparams[1]] > 1:
				cart[request.urlparams[1]] -= 1
			
			else:
				del cart[request.urlparams[1]]
			

			request.session['cart'] = cart
			return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

	for key in cart:
		object = pmod.CatalogProduct.objects.get(id=key)
		Objects[object] = cart[key]

	#for loop that calculates the subtotal adding all the prices of all items in the cart 	
	subtotal = 0
	for key in Objects:
		subtotal += key.price * Objects[key]	

	count = 0
	for key in Objects:
		count += 1
	if count > 0:
		empty = False
	else:
		empty = True

	tvars = {
		'Objects': Objects,
		'empty': empty,
		'subtotal': subtotal,
	}
	return templater.render_to_response(request, 'cart.html', tvars)
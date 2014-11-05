from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater

def process_request(request):
	'''py that handles adding items to cart'''

	pid = request.urlparams[0]
	cart = request.session.get('cart', {})
	if pid in cart:
		cart[pid] += 1
	else:
		cart[pid] = 1
	request.session['cart'] = cart
	return HttpResponseRedirect('/shop/cart')
from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

def process_request(request):
	'''This py handles the checkout process in the shop app'''

	#this if statement makes sure the customer is already logged in before continuing
	# if not looged in the user is redirected to login
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shop/login/checkout')

	#this if statement makes sure the user's account has been confirmed via email.	
	if request.user.confirmed == False:
		return HttpResponseRedirect('/shop/confirmed')

	#gets the cart items from the session	
	cart = request.session.get('cart', {})
	Objects = {}
	
	for key in cart:
		object = pmod.CatalogProduct.objects.get(id=key)
		Objects[object] = cart[key]

	subtotal = 0
	for key in Objects:
		subtotal += key.price * Objects[key]

	if subtotal == 0:
		return HttpResponseRedirect('/shop/cart/')

	user = pmod.User.objects.get(username = request.user.username)
	shippings = pmod.UserShipping.objects.filter(user = user)
	billings = pmod.UserBilling.objects.filter(user = user)
	shippingobject = pmod.UserShipping()
	shippingoptions = pmod.ShippingOption.objects.all()

	needBilling = False
	needShipping = False
	needOption = False
	badcard = False

	#this if statements are used to determine if in the urlparameter, contains 
	#one of the following letters. If so, it trigges one of the booleans. Allowing
	#to raise messages for the user to make sure the have added and selected all
	#the information in order to finisih the checkout process
	if request.urlparams[0]:
		if "b" in request.urlparams[0]:
			needBilling = True
		if "s" in request.urlparams[0]:
			needShipping = True
		if "o" in request.urlparams[0]:
			needOption = True
		if "c" in request.urlparams[0]:
			badcard = True


	possiblesellers = pmod.User.objects.filter(is_staff=True)

	tvars = {
		'Objects': Objects,
		'subtotal': subtotal,
		'shippingobject': shippingobject,
		'shippings': shippings,
		'billings': billings,
		'shippingoptions': shippingoptions,
		'needBilling': needBilling,
		'needShipping': needShipping,
		'needOption': needOption,
		'badcard': badcard,
		'possiblesellers': possiblesellers,
	}
	return templater.render_to_response(request, 'checkout.html', tvars)
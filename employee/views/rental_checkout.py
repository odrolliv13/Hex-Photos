from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view displays the total for the rental and allows the user to make payment

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shop/login/checkout')

	try:
		rental_user = pmod.User.objects.get(id = request.urlparams[0])

	except:
		return HttpResponseRedirect("/employee")

	needBilling = False
	badcard = False
	if request.urlparams[1]:
			if "b" in request.urlparams[1]:
				needBilling = True
			if "c" in request.urlparams[1]:
				badcard = True

	unpaid_rentals = pmod.Rental.objects.filter(user = rental_user, paid=False, return_date__isnull=False)
	userid = rental_user.id

	subtotal = 0

	for i in unpaid_rentals:
		subtotal += i.before_fees + i.late_fees + i.damage_fees


	user = rental_user
	billings = pmod.UserBilling.objects.filter(user = user)


	tvars = {
		'userid': userid,
		'unpaid_rentals': unpaid_rentals,
		'billings': billings,
		'subtotal': subtotal,
		'needBilling': needBilling,
		'badcard': badcard,
	}
	return templater.render_to_response(request, 'rental_checkout.html', tvars)
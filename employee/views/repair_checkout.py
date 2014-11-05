from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view displays the total for the repair and allows the user to make payment

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shop/login/checkout')

	try:
		repair_user = pmod.User.objects.get(id = request.urlparams[0])

	except:
		return HttpResponseRedirect("/employee")

	needBilling = False
	badcard = False
	if request.urlparams[1]:
			if "b" in request.urlparams[1]:
				needBilling = True
			if "c" in request.urlparams[1]:
				badcard = True

	unpaid_repairs = pmod.Repair.objects.filter(user = repair_user, paid=False, date_returned__isnull=False)
	userid = repair_user.id

	subtotal = 0

	for i in unpaid_repairs:
		subtotal += i.total_charged

	user = repair_user
	billings = pmod.UserBilling.objects.filter(user = user)

	tvars = {
		'userid': userid,
		'unpaid_repairs': unpaid_repairs,
		'billings': billings,
		'subtotal': subtotal,
		'needBilling': needBilling,
		'badcard': badcard,
	}
	return templater.render_to_response(request, 'repair_checkout.html', tvars)
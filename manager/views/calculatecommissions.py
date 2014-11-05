from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from manager import models as pmod
import decimal, datetime
from . import templater

# This view calculates the commissions and later displays the total commissions

def process_request(request):
	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/login/')

	thirty = datetime.date.today() - datetime.timedelta(days=30)
	#commissions are calculated thirty days after the sale
	transactions = pmod.Transaction.objects.filter(date__lt=thirty, commissionNeeded=True)

	for t in transactions:
		commission = pmod.Commission()
		commission.transaction = t
		commission.seller = t.seller
		commission.amount = t.seller.commissionRate * t.subtotal
		commission.paid = False
		commission.save()
		t.commissionNeeded = False
		t.save()

	commissions = pmod.Commission.objects.all()

	aggregated = {}

	for c in commissions:
		if c.seller in aggregated:
			aggregated[c.seller] += c.amount
		else:
			aggregated[c.seller] = c.amount

	tvars = {
		'aggregated': aggregated,
	}
	return templater.render_to_response(request, 'calculatecommissions.html', tvars)
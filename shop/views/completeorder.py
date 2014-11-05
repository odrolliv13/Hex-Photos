from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from manager import models as pmod
from . import templater
import decimal, datetime
from django.core.mail import send_mail
import requests
from base_app import payment as gateway

def process_request(request):
	print("Below are the paramaters!")
	print(request.urlparams[0])
	if request.method == 'POST':
		billing = request.POST.get('billing')
		shipping = request.POST.get('shipping')
		shippingoptions = request.POST.get('shippingoptions')
		selleroption = request.POST.get('sellers')		
		redirectParams = ""
		

		# This checks the options for the order. If not the page goes back to checkout and will display the errors
		if billing is None:
			redirectParams += "b"

		if shipping is None:
			redirectParams += "s"

		if shippingoptions is None:
			redirectParams += "o"

		if len(redirectParams) > 0:
			redirect = '/shop/checkout/' + redirectParams
			return HttpResponseRedirect(redirect)


		billing = billing.replace("}","")
		shipping = shipping.replace("}","")
		shippingoptions = shippingoptions.replace("}","")
		


		user = pmod.User.objects.get(username = request.user.username)
		userbilling = pmod.UserBilling.objects.get(user = user, id = billing)
		usershipping = pmod.UserShipping.objects.get(user = user, id = shipping)

		useroption = pmod.ShippingOption.objects.get(id = shippingoptions)

		if selleroption is None:
			seller = pmod.User.objects.get(username = "onlinesale@hexphotos.com")
			sellercommission = False
		else:
			selleroption = selleroption.replace("}","")
			seller = pmod.User.objects.get(id = selleroption)
			sellercommission = True


		transactiontype = pmod.TransactionType.objects.get(transactiontype = "OnlineSale")

		# This gets the taxrate for the customer's state
		try:
			taxRate = pmod.TaxRates.objects.get(state = shipping.state)
		except:
			taxRate = pmod.TaxRates.objects.get(state = "default")


		cart = request.session.get('cart', {})
		Objects = {}
	
		for key in cart:
			object = pmod.CatalogProduct.objects.get(id=key)
			Objects[object] = cart[key]

		subtotal = 0
		for key in Objects:
			subtotal += key.price * Objects[key]

		# Here the payment is checked
		payment_passed = gateway.payment()
		payment_passed.setVariables(userbilling, subtotal, taxRate.taxRate)
		if payment_passed.check() == False:
			redirectParams = "c"
			redirect = '/shop/checkout/' + redirectParams
			return HttpResponseRedirect(redirect)


		transaction = pmod.Transaction()
		transaction.buyer = user
		transaction.seller = seller
		transaction.transactiontype = transactiontype
		transaction.shipping = usershipping
		transaction.billing = userbilling
		transaction.shippingoption = useroption
		transaction.subtotal = subtotal + useroption.price
		transaction.taxAmount = subtotal * taxRate.taxRate
		transaction.date = datetime.datetime.now()
		transaction.commissionNeeded = sellercommission
		transaction.packed = False
		transaction.save()

		cost = 0

		for key in Objects:
			pack = pmod.TransactionToPack()
			pack.transaction = transaction
			pack.catalog_product = key
			pack.quantity = Objects[key]
			pack.packed = False
			pack.save()

		# The journal entry is created here
		journalentry = pmod.JournalEntry()
		journalentry.transaction = transaction
		journalentry.note = "Online Sale to " + user.username + "for $" + str(transaction.subtotal + transaction.taxAmount)
		journalentry.save()

		cashledger = pmod.Subledger.objects.get(type = "Cash")
		saleledger = pmod.Subledger.objects.get(type = "Sales")

		cash = pmod.DebitCredit()
		cash.journalentry = journalentry
		cash.subledger = cashledger
		cash.isDebit = True
		cash.amount = transaction.subtotal + transaction.taxAmount
		cash.save()

		sale = pmod.DebitCredit()
		sale.journalentry = journalentry
		sale.subledger = saleledger
		sale.isDebit = False
		sale.amount = transaction.subtotal + transaction.taxAmount
		sale.save()
			
		cart = {}
		request.session['cart'] = cart

		totalcharged = cash.amount
		
		items = ""
		for key in Objects:
			items += str(key.name) + ": Quantity " + str(Objects[key]) + "\r\n"

		message = user.first_name + " " + user.last_name + ":\r\n" + "We have received a payment of $" + str(cash.amount) + " for the following items:\r\n" + items + "\r\nThank you!\r\n\r\nHexPhotos"
		
		send_mail('HexPhotos Payment Received', message, 'no-reply@hexphotos.com', [user.email], fail_silently=False)


		EndDate = datetime.date.today() + datetime.timedelta(days=useroption.daystoarrive)

		tvars = {
			'Objects': Objects,
			'userbilling': userbilling,
			'usershipping': usershipping,
			'useroption': useroption,
			'totalcharged': totalcharged,
			'EndDate': EndDate,
		}
		return templater.render_to_response(request, 'completeorder.html', tvars)
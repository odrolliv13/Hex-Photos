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

# This view processes the payment and creates transactions and journal entries for a repair

def process_request(request):
	print("Below are the paramaters!")
	print(request.urlparams[0])
	if request.method == 'POST':
		billing = request.POST.get('billing')

		redirectParams = ""
		
		# This checks the options for the order. If not the page goes back to checkout and will display the errors
		if billing is None:
			redirectParams += "b"

		if len(redirectParams) > 0:
			redirect = '/employee/repair_checkout/' + request.urlparams[0] + "/" + redirectParams
			return HttpResponseRedirect(redirect)


		billing = billing.replace("}","")
		


		user = pmod.User.objects.get(id = request.urlparams[0])

		userbilling = pmod.UserBilling.objects.get(user = user, id = billing)


		
		seller = request.user
		sellercommission = False
		


		transactiontype = pmod.TransactionType.objects.get(transactiontype = "Repair")

		# This gets the taxrate for the customer's state
		try:
			taxRate = pmod.TaxRates.objects.get(state = shipping.state)
		except:
			taxRate = pmod.TaxRates.objects.get(state = "default")


	


		subtotal = 0

		unpaid_repairs = pmod.Repair.objects.filter(user = user, paid=False, date_returned__isnull=False)

		for e in unpaid_repairs:
			subtotal += e.total_charged

		# Here the payment is checked
		payment_passed = gateway.payment()
		payment_passed.setVariables(userbilling, subtotal, taxRate.taxRate)
		if payment_passed.check() == False:
			redirectParams = "c"
			redirect = '/employee/repair_checkout/' + request.urlparams[0] + "/" + redirectParams
			return HttpResponseRedirect(redirect)


		transaction = pmod.Transaction()
		transaction.buyer = user
		transaction.seller = seller
		transaction.subtotal = subtotal
		transaction.transactiontype = transactiontype
		transaction.billing = userbilling
		transaction.taxAmount = subtotal * taxRate.taxRate
		transaction.date = datetime.datetime.now()
		transaction.commissionNeeded = sellercommission
		transaction.save()

		cost = 0
		
		for e in unpaid_repairs:
			e.paid = True
			e.save()
			rt = pmod.RepairTransaction()
			rt.transaction = transaction
			rt.repair = e
			rt.save()
			cost = e.estimate + e.cost
	


		# The journal entry is created here
		journalentry = pmod.JournalEntry()
		journalentry.transaction = transaction
		journalentry.note = "Rental to " + user.username + "for $" + str(transaction.subtotal + transaction.taxAmount)
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


		totalcharged = cash.amount
		
		items = ""
		for e in unpaid_repairs:
			items += "Repair for Item " + e.serial_number + "\r\n   Description: " + e.description + "\r\n    Problem: " + e.problem + "\r\n"

		message = user.first_name + " " + user.last_name + ":\r\n" + "We have received a payment of $" + str(cash.amount) + " for follwing items:\r\n" + items + "\r\nThank you!\r\n\r\nHexPhotos"
		
		send_mail('HexPhotos Payment Received', message, 'no-reply@hexphotos.com', [user.email], fail_silently=True)


		tvars = {
			'unpaid_repairs': unpaid_repairs,
			'userbilling': userbilling,
			'totalcharged': totalcharged,
		}
		return templater.render_to_response(request, 'repair_complete_order.html', tvars)
from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view allows an employee to gather the physical items for a customer's online transaction.

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/employee/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/employee/')

	if request.urlparams[0]:
	 	transaction = pmod.Transaction.objects.get(id = request.urlparams[0])


	items = pmod.TransactionToPack.objects.filter(transaction = transaction, packed=False)
	# This gets all the unpacked items for a given transaction
	item = None
	for i in items:
		# this look grabs the first unpacked item and then creates a form 
		item = i
		if i.catalog_product.inventorytype.name == "Stocked":
			form = StockedProductForm(i, initial ={
				'serial_number': "",
			})
			print
		else:
			form = SerializedProductForm(i, initial ={
				'serial_number': "",
			})
		break

	if request.method == 'POST':
		if item.catalog_product.inventorytype.name == "Stocked":
			form = StockedProductForm(item, request.POST)
			if form.is_valid():
				stocked_transaction = pmod.StockedTransaction()
				stocked_transaction.transaction = item.transaction
				stocked_transaction.stocked = form.cleaned_data['serial_number']
				stocked_transaction.amount = item.quantity
				stocked_transaction.save()
				item.packed = True
				item.save()
				form.cleaned_data['serial_number'].amount -= item.quantity
				form.cleaned_data['serial_number'].save()
				items = pmod.TransactionToPack.objects.filter(transaction = transaction, packed=False)
				count = 0
				for i in items:
					count += 1
				if count > 0:
					return HttpResponseRedirect('/manager/pack_order/' + str(transaction.id))
				else:
					item.transaction.packed = True
					item.transaction.save()
					return HttpResponseRedirect('/manager/online_orders/')
		else:
			form = SerializedProductForm(item, request.POST)
			if form.is_valid():
				serialized_transaction = pmod.SerializedTransaction()
				serialized_transaction.transaction = item.transaction
				serialized_transaction.serialized = form.cleaned_data['serial_number']
				serialized_transaction.save()
				item.quantity -= 1
				if item.quantity == 0:
					item.packed = True
				item.save()
				form.cleaned_data['serial_number'].is_available = False
				form.cleaned_data['serial_number'].datePurchased = datetime.datetime.now()
				form.cleaned_data['serial_number'].is_active = False
				form.cleaned_data['serial_number'].save()

				items = pmod.TransactionToPack.objects.filter(transaction = transaction, packed=False)
				count = 0
				for i in items:
					count += 1
				if count > 0:
					return HttpResponseRedirect('/manager/pack_order/' + str(transaction.id))
				else:
					item.transaction.packed = True
					item.transaction.save()
					return HttpResponseRedirect('/manager/online_orders/')
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'pack_order.html', tvars)

class SerializedProductForm(forms.Form):
	serial_number = forms.ModelChoiceField(queryset=pmod.SerializedProduct.objects.filter(is_rental=False, is_available=True), label="Serial Number", widget=forms.Select(attrs={'class':'form-control'}))

	def __init__(self, item,*args, **kwargs):
		super(SerializedProductForm, self).__init__(*args, **kwargs)
		self.fields['serial_number'].queryset = pmod.SerializedProduct.objects.filter(is_rental=False, is_available=True, catalogID=item.catalog_product)

class StockedProductForm(forms.Form):
	serial_number = forms.ModelChoiceField(queryset=pmod.StockedProduct.objects.filter(is_active=True), label="Serial Number", widget=forms.Select(attrs={'class':'form-control'}))

	def __init__(self, item,*args, **kwargs):
		super(StockedProductForm, self).__init__(*args, **kwargs)
		self.item = item
		self.fields['serial_number'].queryset = pmod.StockedProduct.objects.filter(is_active=True, catalogID=item.catalog_product)

	def clean(self):
		if self.item.quantity <= self.cleaned_data['serial_number'].amount:
			pass
		else:
			raise forms.ValidationError("There are not enough items in stock")
		return self.cleaned_data
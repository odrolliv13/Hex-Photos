from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view will display all the catalog products. From here an employee can choose one and then get a list of the available products of that type to rent

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/employee/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/shop/')

	'''Shows the list of users'''
	form = LookupRentalForm(initial ={
		'item': "",
		})
	
	if request.method == 'POST':
		form = LookupRentalForm(request.POST)
		if form.is_valid():
			rental_item = pmod.CatalogProduct.objects.get(name = form.cleaned_data['item'].name)
			redirect = "/employee/new_rental/" + str(rental_item.id)
			return HttpResponseRedirect(redirect)
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'lookup_rental.html', tvars)

class LookupRentalForm(forms.Form):
	type = pmod.InventoryType.objects.get(name="Stocked")
	print(type)
	item = forms.ModelChoiceField(queryset=pmod.CatalogProduct.objects.exclude(inventorytype=type, is_active=False), label="Catalog Product", widget=forms.Select(attrs={'class':'form-control'}))
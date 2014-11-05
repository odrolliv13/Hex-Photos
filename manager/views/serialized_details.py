from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This page allows an employee to make or edit a serialized product

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/')

	'''Shows the list of users'''
	if request.urlparams[0] == "new":

		form = SerializedProductForm(initial ={
				'catalogID': "",
				'store': "",
				'serialNumber': "",
				'cost': "",
				'datePurchased': "",
				'is_rental': "",
				'is_available': "",
				'is_new': "",
				})
	

	else:
		user = pmod.SerializedProduct.objects.get(id=request.urlparams[0])

		form = SerializedProductForm(initial ={
			'catalogID': user.catalogID,
			'store': user.store,
			'serialNumber': user.serialNumber,
			'cost': user.cost,
			'datePurchased': user.datePurchased,
			'is_rental': user.is_rental,
			'is_available': user.is_available,
			'is_new': user.is_new,
			})
	
	if request.method == 'POST':
		form = SerializedProductForm(request.POST)
		if form.is_valid():
			if request.urlparams[0] == "new":
				user = pmod.SerializedProduct()
			user.catalogID = form.cleaned_data['catalogID']
			user.store = form.cleaned_data['store']
			user.serialNumber = form.cleaned_data['serialNumber']
			user.cost = form.cleaned_data['cost']
			user.datePurchased = form.cleaned_data['datePurchased']
			user.is_rental = form.cleaned_data["is_rental"]
			user.is_available = form.cleaned_data['is_available']
			user.is_new = form.cleaned_data['is_new']
			user.is_active = True
			user.save()
			return HttpResponseRedirect('/manager/serialized_inventory')
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'serialized_details.html', tvars)

class SerializedProductForm(forms.Form):
	catalogID = forms.ModelChoiceField(queryset=pmod.CatalogProduct.objects.exclude(is_active=False), label="Catalog Item", widget=forms.Select(attrs={'class':'form-control'}))
	store = forms.ModelChoiceField(queryset=pmod.Store.objects.exclude(active=False), label="Store", widget=forms.Select(attrs={'class':'form-control'}))
	serialNumber = forms.CharField(required=False, label='Serial Number', widget=forms.TextInput(attrs={'class':'form-control'}))
	datePurchased = forms.DateField(required=False, label='Date Purchased', widget=forms.TextInput(attrs={'class':'form-control'}))
	cost = forms.DecimalField(required=False, label='Cost', widget=forms.TextInput(attrs={'class':'form-control'}))
	is_rental = forms.NullBooleanField(required=False, label='Rental', widget=forms.NullBooleanSelect(attrs={'class':'form-control'}))
	is_available = forms.NullBooleanField(required=False, label='Available', widget=forms.NullBooleanSelect(attrs={'class':'form-control'}))
	is_new = forms.NullBooleanField(required=False, label='New', widget=forms.NullBooleanSelect(attrs={'class':'form-control'}))
	#def clean_user_text(self):
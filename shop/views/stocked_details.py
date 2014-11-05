from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/')


	'''Shows the list of users'''
	if request.urlparams[0] == "new":

		form = StockedProductForm(initial ={
				'catalogID': "",
				'store': "",
				'amount': "",
				'cost': "",
				})
	else:
		user = pmod.StockedProduct.objects.get(id=request.urlparams[0])

		form = StockedProductForm(initial ={
			'catalogID': user.catalogID,
			'store': user.store,
			'amount': user.amount,
			'cost': user.cost,
			})
	
	if request.method == 'POST':
		form = StockedProductForm(request.POST)
		if form.is_valid():
			if request.urlparams[0] == "new":
				user = pmod.StockedProduct()
			user.catalogID = form.cleaned_data['catalogID']
			user.store = form.cleaned_data['store']
			user.amount = form.cleaned_data['amount']
			user.cost = form.cleaned_data['cost']
			user.is_active = True
			user.save()
			return HttpResponseRedirect('/manager/stocked_inventory')

	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'stocked_details.html', tvars)

class StockedProductForm(forms.Form):
	catalogID = forms.ModelChoiceField(queryset=pmod.CatalogProduct.objects.exclude(is_active=False), label="Catalog Item", widget=forms.Select(attrs={'class':'form-control'}))
	store = forms.ModelChoiceField(queryset=pmod.Store.objects.exclude(active=False), label="Store", widget=forms.Select(attrs={'class':'form-control'}))
	amount = forms.IntegerField(required=False, label='Amount', widget=forms.TextInput(attrs={'class':'form-control'}))
	cost = forms.DecimalField(required=False, label='Cost', widget=forms.TextInput(attrs={'class':'form-control'}))
	#def clean_user_text(self):
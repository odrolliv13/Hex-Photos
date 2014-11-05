from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This page allows an employee to make or edit a store

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/')
	
	'''Shows the list of stores'''
	if request.urlparams[0] == "new":
		form = StoreForm(initial ={
			'locationName': "",
			'manager': "",
			'street': "",
			'city': "",
			'state': "",
			'zipcode': "",
			'phone': "",
			})
	else:
		store = pmod.Store.objects.get(id=request.urlparams[0])

		form = StoreForm(initial ={
			'locationName': store.locationName,
			'manager': store.manager,
			'street': store.street,
			'city': store.city,
			'state': store.state,
			'zipcode': store.zipcode,
			'phone': store.phone,
			})
	
	if request.method == 'POST':
		form = StoreForm(request.POST)
		if form.is_valid():
			if request.urlparams[0] == "new":
				store = pmod.Store()
			store.locationName = form.cleaned_data['locationName']
			store.manager = form.cleaned_data['manager']
			store.street = form.cleaned_data['street']
			store.city = form.cleaned_data['city']
			store.state = form.cleaned_data['state']
			store.zipcode = form.cleaned_data['zipcode']
			store.phone = form.cleaned_data['phone']
			store.active = True
			store.save()
			return HttpResponseRedirect('/manager/stores')
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'store_details.html', tvars)

class StoreForm(forms.Form):
	locationName = forms.CharField(required=False, label='Location Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	manager = forms.ModelChoiceField(queryset=pmod.User.objects.filter(is_staff=True), label="Manager", widget=forms.Select(attrs={'class':'form-control'}))
	street = forms.CharField(required=False, label='Street', widget=forms.TextInput(attrs={'class':'form-control'}))
	city  = forms.CharField(required=False, label='City', widget=forms.TextInput(attrs={'class':'form-control'}))
	state  = forms.CharField(required=False, label='State', widget=forms.TextInput(attrs={'class':'form-control'}))
	zipcode  = forms.CharField(required=False, label='Zipcode', widget=forms.TextInput(attrs={'class':'form-control'}))
	phone  = forms.CharField(required=False, label='Phone', widget=forms.TextInput(attrs={'class':'form-control'}))
	#def clean_store_text(self):
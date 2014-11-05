from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from . import templater
from django.conf import settings
from manager import models as pmod
import decimal, datetime

#This view allows an employee to create a new billing option for a customer that they are checking out for a rental or a repair order

def process_request(request):
	if request.user.is_staff == False:
		return HttpResponseRedirect('/shop/')

	form = BillingForm(initial ={
		'name': "",
		'cardtype': "",
		'number': "",
		'security': "",
		'street': "",
		'city': "",
		'state': "",
		'zipcode': "",
		'expmonth': "",
		'expyear': "",
		})

	if request.method == 'POST':
		form = BillingForm(request.POST)
		if form.is_valid():
			user = pmod.User.objects.get(id = request.urlparams[0])
			billing = pmod.UserBilling()
			billing.user = user
			billing.name = form.cleaned_data['name']
			billing.cardtype = form.cleaned_data['cardtype']
			billing.number = form.cleaned_data['number']
			billing.security = form.cleaned_data['security']
			billing.street = form.cleaned_data['street']
			billing.city = form.cleaned_data['city']
			billing.state = form.cleaned_data['state']
			billing.zipcode = form.cleaned_data['zipcode']
			billing.expmonth = form.cleaned_data['expmonth']
			billing.expyear = form.cleaned_data['expyear']
			billing.save()
			
			# From here the page will be redirected to whatever checkout the employee was doing at the time of adding a new payment
			if request.urlparams[1] == "rental_checkout":
				redirect = "/employee/rental_checkout/" + str(request.urlparams[0])
				return HttpResponseRedirect(redirect)
			else:
				redirect = "/employee/repair_checkout/" + str(request.urlparams[0])
				return HttpResponseRedirect(redirect)
	
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'billing_details.html', tvars)

class BillingForm(forms.Form):
	name = forms.CharField(required=False, label='Name on Card', widget=forms.TextInput(attrs={'class':'form-control'}))
	cardtype = forms.ModelChoiceField(queryset=pmod.CardType.objects.all(), label="Card Type", widget=forms.Select(attrs={'class':'form-control'}))
	number = forms.CharField(required=False, label='Card Number', widget=forms.TextInput(attrs={'class':'form-control'}))
	security = forms.CharField(required=False, label='Security Code', widget=forms.TextInput(attrs={'class':'form-control'}))
	street = forms.CharField(required=False, label='Street', widget=forms.TextInput(attrs={'class':'form-control'}))
	city  = forms.CharField(required=False, label='City', widget=forms.TextInput(attrs={'class':'form-control'}))
	state  = forms.CharField(required=False, label='State', widget=forms.TextInput(attrs={'class':'form-control'}))
	zipcode  = forms.CharField(required=False, label='Zipcode', widget=forms.TextInput(attrs={'class':'form-control'}))
	expmonth = forms.IntegerField(required=False, label="Exp. Month", min_value=1, max_value=12, widget=forms.TextInput(attrs={'class':'form-control'}))
	expyear = forms.IntegerField(required=False, label="Exp. Year",min_value=1, widget=forms.TextInput(attrs={'class':'form-control'}))
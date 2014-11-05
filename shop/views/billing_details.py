from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from . import templater
from django.conf import settings
from manager import models as pmod
import decimal, datetime

def process_request(request):
	'''this py handles the billing details of a customer. '''
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shop/login')
	if request.urlparams[0]:
		if request.urlparams[0] != "checkout":
			billing = pmod.UserBilling.objects.get(id=request.urlparams[0])

			form = BillingForm(initial ={
				'name': billing.name,
				'cardtype': billing.cardtype,
				'number': billing.number,
				'security': billing.security,
				'street': billing.street,
				'city': billing.city,
				'state': billing.state,
				'zipcode': billing.zipcode,
				'expmonth': billing.expmonth,
				'expyear': billing.expyear,
				})
		else:
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
	else:
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
		form = BillingForm(request.POST, request=request)
		if form.is_valid():
			if not request.urlparams[0] or request.urlparams[0] == "checkout":
				user = pmod.User.objects.get(username = request.user.username)
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
			if request.urlparams[0] == "checkout" or request.urlparams[1] == "checkout":
				return HttpResponseRedirect('/shop/checkout')
			return HttpResponseRedirect('/shop/account/billing')
	
	
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



	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(BillingForm, self).__init__(*args, **kwargs)
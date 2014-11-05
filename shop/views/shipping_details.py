from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from . import templater
from django.conf import settings
from manager import models as pmod
import decimal, datetime

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shop/login')
	if request.urlparams[0]:
		if request.urlparams[0] != "checkout":
			shipping = pmod.UserShipping.objects.get(id=request.urlparams[0])

			form = ShippingForm(initial ={
				'name': shipping.name,
				'street': shipping.street,
				'city': shipping.city,
				'state': shipping.state,
				'zipcode': shipping.zipcode,
				})
		else:
			form = ShippingForm(initial ={
				'name': "",
				'street': "",
				'city': "",
				'state': "",
				'zipcode': "",
				})
	else:
		form = ShippingForm(initial ={
			'name': "",
			'street': "",
			'city': "",
			'state': "",
			'zipcode': "",
			})
	if request.method == 'POST':
		form = ShippingForm(request.POST, request=request)
		if form.is_valid():
			if not request.urlparams[0] or request.urlparams[0] == "checkout":
				user = pmod.User.objects.get(username = request.user.username)
				shipping = pmod.UserShipping()
				shipping.user = user
			shipping.name = form.cleaned_data['name']
			shipping.street = form.cleaned_data['street']
			shipping.city = form.cleaned_data['city']
			shipping.state = form.cleaned_data['state']
			shipping.zipcode = form.cleaned_data['zipcode']
			shipping.save()
			if request.urlparams[0] == "checkout" or request.urlparams[1] == "checkout":
				return HttpResponseRedirect('/shop/checkout')
			return HttpResponseRedirect('/shop/account/shipping')
	
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'shipping_details.html', tvars)

class ShippingForm(forms.Form):
	name = forms.CharField(required=False, label='Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	street = forms.CharField(required=False, label='Street', widget=forms.TextInput(attrs={'class':'form-control'}))
	city  = forms.CharField(required=False, label='City', widget=forms.TextInput(attrs={'class':'form-control'}))
	state  = forms.CharField(required=False, label='State', widget=forms.TextInput(attrs={'class':'form-control'}))
	zipcode  = forms.CharField(required=False, label='Zipcode', widget=forms.TextInput(attrs={'class':'form-control'}))

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ShippingForm, self).__init__(*args, **kwargs)
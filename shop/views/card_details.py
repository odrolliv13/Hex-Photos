from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from . import templater
from django.conf import settings
import decimal, datetime

def process_request(request):
	'''handles the form for a customer to edit and add their credit card information'''


	form = UserForm(initial ={
		'name': "",
		'card': "",
		'number': "",
		'security': "",
		'street': "",
		'city': "",
		'state': "",
		'zipcode': "",
		'country': "",
		})
	
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'card_details.html', tvars)

class UserForm(forms.Form):
	name = forms.CharField(required=False, label='Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	card = forms.ChoiceField(choices = ([('1','Select a Card'), ('2','Discover'),('3','Mastercard'),('4','Visa'), ]), label="Card Type", widget=forms.Select(attrs={'class':'form-control'}))
	number = forms.CharField(required=False, label='Card Number', widget=forms.TextInput(attrs={'class':'form-control'}))
	security = forms.CharField(required=False, label='Security Code', widget=forms.TextInput(attrs={'class':'form-control'}))
	street = forms.CharField(required=False, label='Street', widget=forms.TextInput(attrs={'class':'form-control'}))
	city  = forms.CharField(required=False, label='City', widget=forms.TextInput(attrs={'class':'form-control'}))
	state  = forms.ChoiceField(choices = ([('1','Select a State')]), label="State", widget=forms.Select(attrs={'class':'form-control'}))
	zipcode  = forms.CharField(required=False, label='Zipcode', widget=forms.TextInput(attrs={'class':'form-control'}))
	country = forms.ChoiceField(choices = ([('1','Select a Country')]), label="Country", widget=forms.Select(attrs={'class':'form-control'}))
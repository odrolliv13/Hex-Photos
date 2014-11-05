from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from shop import models as pmod
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
		user = pmod.CatalogProduct()
		user.catalogID = ""
		user.name = ""
		user.description = ""
		user.brand = ""
		user.category = ""
		user.commissionRate = 0
		user.rentalPrice = 0
		user.replacementPrice = 0
		user.is_active = True
	else:
		user = pmod.CatalogProduct.objects.get(id=request.urlparams[0])

	form = CatalogProductForm(initial ={
		'catalogID': user.catalogID,
		'name': user.name,
		'description': user.description,
		'brand': user.brand,
		'category': user.category,
		'commissionRate': user.commissionRate,
		'rentalPrice': user.rentalPrice,
		'replacementPrice': user.replacementPrice,
		})
	
	if request.method == 'POST':
		form = CatalogProductForm(request.POST)
		if form.is_valid():
			user.catalogID = form.cleaned_data['catalogID']
			user.name = form.cleaned_data['name']
			user.lname = user.name.lower()
			user.description = form.cleaned_data['description']
			user.ldescription = user.description.lower()
			user.brand = form.cleaned_data['brand']
			user.lbrand = user.brand.lower()
			user.category = form.cleaned_data['category']
			user.commissionRate = form.cleaned_data['commissionRate']
			user.rentalPrice = form.cleaned_data['rentalPrice']
			user.replacementPrice = form.cleaned_data['replacementPrice']
			user.is_active = True
			user.save()
			return HttpResponseRedirect('/manager/catalog_products')
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'user_details.html', tvars)

class CatalogProductForm(forms.Form):
	catalogID = forms.CharField(required=False, label='CatalogID', widget=forms.TextInput(attrs={'class':'form-control'}))
	name = forms.CharField(required=False, label='Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	description = forms.CharField(required=False, label='Description', widget=forms.TextInput(attrs={'class':'form-control'}))
	brand = forms.CharField(required=False, label='Brand', widget=forms.TextInput(attrs={'class':'form-control'}))
	category  = forms.CharField(required=False, label='Category', widget=forms.TextInput(attrs={'class':'form-control'}))
	commissionRate  = forms.DecimalField(required=False, label='Comission Rate', widget=forms.TextInput(attrs={'class':'form-control'}))
	rentalPrice  = forms.DecimalField(required=False, label='Rental Price', widget=forms.TextInput(attrs={'class':'form-control'}))
	replacementPrice = forms.DecimalField(required=False, label='Replacement Price', widget=forms.TextInput(attrs={'class':'form-control'}))
	#def clean_user_text(self):
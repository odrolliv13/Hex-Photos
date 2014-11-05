from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view checks the details of a CatalogProduct
# New CatalogProducts are also made using this form

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/')

	'''Shows the list of users'''
	if request.urlparams[0] == "new":
		form = CatalogProductForm(initial ={
			'catalogID': "",
			'inventorytype': "",
			'name': "",
			'description': "",
			'brand': "",
			'category': "",
			'imagepath': "",
			'price': "",
			'rentalPrice': "",
			'replacementPrice': "",
			})
	else:
		user = pmod.CatalogProduct.objects.get(id=request.urlparams[0])

		form = CatalogProductForm(initial ={
			'catalogID': user.catalogID,
			'inventorytype': user.inventorytype,
			'name': user.name,
			'description': user.description,
			'brand': user.brand,
			'category': user.category,
			'imagepath': user.imagePath,
			'price': user.price,
			'rentalPrice': user.rentalPrice,
			'replacementPrice': user.replacementPrice,
			})
	
	if request.method == 'POST':
		form = CatalogProductForm(request.POST)
		if form.is_valid():
			if request.urlparams[0] == "new":
				user = pmod.CatalogProduct()
			user.catalogID = form.cleaned_data['catalogID']
			user.inventorytype = form.cleaned_data['inventorytype']
			user.imagePath = form.cleaned_data['imagepath']
			user.name = form.cleaned_data['name']
			user.description = form.cleaned_data['description']
			user.brand = form.cleaned_data['brand']
			user.category = form.cleaned_data['category']
			user.price = form.cleaned_data['price']
			user.rentalPrice = form.cleaned_data['rentalPrice']
			user.replacementPrice = form.cleaned_data['replacementPrice']
			user.is_active = True
			user.save()
			return HttpResponseRedirect('/manager/catalog_products')
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'catalog_product_details.html', tvars)

class CatalogProductForm(forms.Form):
	catalogID = forms.CharField(required=False, label='CatalogID', widget=forms.TextInput(attrs={'class':'form-control'}))
	inventorytype = forms.ModelChoiceField(queryset=pmod.InventoryType.objects.all(), label="Inventory Type", widget=forms.Select(attrs={'class':'form-control'}))
	name = forms.CharField(required=False, label='Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	imagepath = forms.CharField(required=False, label='Image Path', widget=forms.TextInput(attrs={'class':'form-control'}))
	description = forms.CharField(required=False, label='Description', widget=forms.TextInput(attrs={'class':'form-control'}))
	brand = forms.CharField(required=False, label='Brand', widget=forms.TextInput(attrs={'class':'form-control'}))
	category  = forms.ModelChoiceField(queryset=pmod.Category.objects.filter(is_active=True), label="Category", widget=forms.Select(attrs={'class':'form-control'}))
	price  = forms.DecimalField(required=False, label='Price', widget=forms.TextInput(attrs={'class':'form-control'}))
	rentalPrice  = forms.DecimalField(required=False, label='Rental Price', widget=forms.TextInput(attrs={'class':'form-control'}))
	replacementPrice = forms.DecimalField(required=False, label='Replacement Price', widget=forms.TextInput(attrs={'class':'form-control'}))
	#def clean_user_text(self):
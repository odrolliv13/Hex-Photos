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
	
	'''Shows the list of stores'''
	if request.urlparams[0] == "new":
		store = pmod.Category()
		store.name = ""
		store.description = ""
		store.imagePath = ""
		store.url = ""

	else:
		store = pmod.Category.objects.get(id=request.urlparams[0])

	form = StoreForm(initial ={
		'name': store.name,
		'description': store.description,
		})
	
	if request.method == 'POST':
		form = StoreForm(request.POST)
		if form.is_valid():
			store.name = form.cleaned_data['name']
			store.description = form.cleaned_data['description']
			store.is_active = True
			store.save()
			return HttpResponseRedirect('/manager/categories')
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'category_details.html', tvars)

class StoreForm(forms.Form):
	name = forms.CharField(required=False, label='Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	description = forms.CharField(required=False, label='Description', widget=forms.TextInput(attrs={'class':'form-control'}))
	#def clean_store_text(self):
from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view will display information regarding a completed repair. After verifying, the page will go to checkout to charge the customer.

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/')

	if request.urlparams[0]:
		repair = pmod.Repair.objects.get(id = request.urlparams[0])

	'''Shows the list of users'''
	form = PickupRepair(initial ={
		'user': repair.user.first_name + " " + repair.user.last_name,
		'serial_number': repair.serial_number,
		'description': repair.description,
		'problem': repair.problem,
		'estimate': repair.estimate,
		'additional_cost': repair.additional_cost,
		'costs_note': repair.costs_note,
		})

		

	if request.method == 'POST':
			form = PickupRepair(request.POST)
			if form.is_valid():
				repair = pmod.Repair.objects.get(id = request.urlparams[0])
				repair.date_returned = datetime.datetime.today()
				repair.total_charged = repair.estimate + repair.additional_cost
				repair.save()
				redirect = "/employee/repair_checkout/" + str(repair.user.id)
				return HttpResponseRedirect(redirect)
	

	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'pickup_repair.html', tvars)

class PickupRepair(forms.Form):
	user = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	serial_number = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	description = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	problem = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	estimate = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	additional_cost = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	costs_note = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	#def clean_user_text(self):
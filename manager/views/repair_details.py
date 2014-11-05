from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view shows the details of a repair and allow an employee to add costs and set the repair to completed

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
		'cost': repair.cost,
		'costs_note': repair.costs_note,
		'status': '',
		})

		

	if request.method == 'POST':
			form = PickupRepair(request.POST)
			if form.is_valid():
				repair = pmod.Repair.objects.get(id = request.urlparams[0])
				repair.additional_cost = form.cleaned_data['additional_cost']
				repair.cost = form.cleaned_data['cost']
				repair.costs_note = form.cleaned_data['costs_note']
				status = pmod.RepairStatus.objects.get(status = form.cleaned_data['status'])
				repair.status = status
				repair.save()
				redirect = "/manager/repairs"
				return HttpResponseRedirect(redirect)
	

	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'repair_details.html', tvars)

class PickupRepair(forms.Form):
	user = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	serial_number = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	description = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	problem = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	estimate = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	additional_cost = forms.DecimalField(required=False, label='Additional Cost for Customer', widget=forms.TextInput(attrs={'class':'form-control'}))
	cost = forms.DecimalField(required=False, label='Actual Cost', widget=forms.TextInput(attrs={'class':'form-control'}))
	costs_note = forms.CharField(label='Costs Note', widget=forms.TextInput(attrs={'class':'form-control'}))
	status = forms.ModelChoiceField(queryset=pmod.RepairStatus.objects.all(), label="Status", widget=forms.Select(attrs={'class':'form-control'}))
	#def clean_user_text(self):
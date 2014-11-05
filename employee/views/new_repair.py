from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view will allow an employee to check in an item for repair. They will input the customer and the information regarding the repair

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/employee/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/employee/')

	'''Shows the list of users'''
	form = NewRepairForm(initial ={
		'user': "",
		'serial_number': "",
		'description': "",
		'problem': "",
		'estimate': "",
		})
	
	if request.method == 'POST':
		form = NewRepairForm(request.POST)
		if form.is_valid():
			repair = pmod.Repair()
			repair.user = form.cleaned_data['user']
			repair.serial_number = form.cleaned_data['serial_number']
			repair.description = form.cleaned_data['description']
			repair.problem = form.cleaned_data['problem']
			repair.estimate = form.cleaned_data['estimate']
			repair.additional_cost = 0
			repair.cost = 0
			repair.costs_note = ""
			repairstatus = pmod.RepairStatus.objects.get(status = "In Progress")
			repair.status = repairstatus
			repair.date_received = datetime.datetime.now()
			repair.paid = False
			repair.save()
			tvars = {
				'repair': repair,
			}
			return templater.render_to_response(request, 'item_repair.html', tvars)
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'new_repair.html', tvars)

class NewRepairForm(forms.Form):
	user = forms.ModelChoiceField(queryset=pmod.User.objects.exclude(is_active=False), label="User", widget=forms.Select(attrs={'class':'form-control'}))
	serial_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
	description = forms.CharField(label = 'Product',required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
	problem = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
	estimate = forms.DecimalField(required=False, label='Estimate', widget=forms.TextInput(attrs={'class':'form-control'}))

	def clean(self):
		if len(self.cleaned_data["serial_number"]) < 1:
			raise forms.ValidationError("You must provide a serial number")
		if len(self.cleaned_data["description"]) < 1:
			raise forms.ValidationError("You must provide a description")
		if len(self.cleaned_data["problem"]) < 1:
			raise forms.ValidationError("You must describe the problem")	
		if self.cleaned_data['estimate'] == 0:
			raise forms.ValidationError("You must provide a valid estimate.")
		return self.cleaned_data
from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view allows an employee to return a rental from a customer. They will be able to input the damage note and fees if necessary, as well as record the return condition

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/')

	if request.urlparams[0]:
		rental = pmod.Rental.objects.get(id = request.urlparams[0])

	days_late = datetime.datetime.now().replace(tzinfo=None) - rental.expected_date.replace(tzinfo=None)
				
	if days_late.days > 0:
		late_fees = rental.daily_rate * 2 * days_late.days
	else:
		late_fees = 0

	'''Shows the list of users'''
	form = ReturnRental(initial ={
		'user': rental.user.first_name + " " + rental.user.last_name,
		'serial_number': rental.serialized.serialNumber,
		'description': rental.serialized.catalogID.name,
		'checkout_date': rental.checkout_date.strftime('%b %d, %Y'),
		'expected_date': rental.expected_date.strftime('%b %d, %Y'),
		'checkout_condition': rental.checkout_condition,
		'return_condition': "",
		'regular_charge': "$" + str(rental.daily_rate * rental.days_to_rent),
		'late_fees': "$" + str(late_fees),
		'damage_note': "",
		'damage_fees': "",
		})

		

	if request.method == 'POST':
			form = ReturnRental(request.POST)
			if form.is_valid():
				rental = pmod.Rental.objects.get(id = request.urlparams[0])
				rental.return_date = datetime.datetime.today()
				rental.before_fees = rental.daily_rate * rental.days_to_rent
				days_late = rental.return_date.replace(tzinfo=None) - rental.expected_date.replace(tzinfo=None)
				
				if days_late.days > 0:
					rental.late_fees = rental.daily_rate * 2 * days_late.days
				else:
					rental.late_fees = 0

				rental.damage_fees = form.cleaned_data['damage_fees']
				rental.damage_note = form.cleaned_data['damage_note']
				rental.return_condition = form.cleaned_data['return_condition']
				rental.save()
				rental.serialized.is_available = True
				rental.serialized.save()
				redirect = "/employee/rental_checkout/" + str(rental.user.id)
				return HttpResponseRedirect(redirect)
	

	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'return_rental.html', tvars)

class ReturnRental(forms.Form):
	user = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	serial_number = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	description = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	checkout_date = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	expected_date = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	checkout_condition = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	return_condition = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
	regular_charge = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	late_fees = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	damage_note = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
	damage_fees = forms.DecimalField(required=False, label='Damage Fee', widget=forms.TextInput(attrs={'class':'form-control'}))
	#def clean_user_text(self):
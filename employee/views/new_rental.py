from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view allows an employee to rent an item to a customer. They will have a dropdown menu of customers, available rental items.
# They will record the condition and then specify the days to rent. Customers will be charged upon return for the whole period that they chose to rent

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/employee/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/employee/')

	rental_item = pmod.CatalogProduct.objects.get(id = request.urlparams[0])

	'''Shows the list of users'''
	form = NewRentalForm(rental_item, initial ={
		'user': "",
		'serial_number': "",
		'condition': "",
		'days_to_rent': "",
		})
	
	if request.method == 'POST':
		form = NewRentalForm(rental_item, request.POST)
		if form.is_valid():
			rental = pmod.Rental()
			rental.user = form.cleaned_data['user']
			form.cleaned_data['serial_number'].is_available = False
			form.cleaned_data['serial_number'].save()
			rental.serialized = form.cleaned_data['serial_number']
			rental.daily_rate = form.cleaned_data['serial_number'].catalogID.rentalPrice
			rental.checkout_condition = form.cleaned_data['condition']
			rental.checkout_date = datetime.datetime.today()
			rental.days_to_rent = form.cleaned_data['days_to_rent']
			rental.expected_date = datetime.datetime.today() + datetime.timedelta(days=form.cleaned_data['days_to_rent'])
			rental.paid = False
			rental.save()
			tvars = {
				'rental': rental,
			}
			return templater.render_to_response(request, 'item_rented.html', tvars)
	
	tvars = {
		'form': form,
		'rental_item': rental_item,
	}
	return templater.render_to_response(request, 'new_rental.html', tvars)

class NewRentalForm(forms.Form):
	user = forms.ModelChoiceField(queryset=pmod.User.objects.exclude(is_active=False), label="User", widget=forms.Select(attrs={'class':'form-control'}))
	serial_number = forms.ModelChoiceField(queryset=pmod.SerializedProduct.objects.filter(is_rental=True, is_available=True), label="Serial Number", widget=forms.Select(attrs={'class':'form-control'}))
	condition = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
	days_to_rent = forms.IntegerField(required=False, min_value=1, widget=forms.TextInput(attrs={'class':'form-control'}))

	def __init__(self, rental_item,*args, **kwargs):
		super(NewRentalForm, self).__init__(*args, **kwargs)
		self.fields['serial_number'].queryset = pmod.SerializedProduct.objects.filter(is_rental=True, is_available=True, catalogID=rental_item)

	def clean(self):
		if len(self.cleaned_data["condition"]) < 5:
			raise forms.ValidationError("You must record condition of the item. (10 Chars)")
		try:
			check = self.cleaned_data['days_to_rent'] + 1
		except TypeError:
			raise forms.ValidationError("You must enter a whole positive number.")
		if self.cleaned_data['days_to_rent'] == 0:
			raise forms.ValidationError("You rent for at least one day.")
		return self.cleaned_data
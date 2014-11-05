from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view will display all users and then on a new page display all the current rentals for a given user

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shop')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/shop')

	if request.urlparams[0] == "":
		
		#This form will display all users
		form = CheckRentalForm(initial ={
			'user': "",
		})
		
		if request.method == 'POST':
			form = CheckRentalForm(request.POST)
			if form.is_valid():
				#From here the page will redirect to show all the current rentals for the user picked
				complete = "/employee/customer_rentals/" + str(form.cleaned_data['user'].id)
				return HttpResponseRedirect(complete)
		
		tvars = {
			'form': form,
		}
		return templater.render_to_response(request, 'return_rental.html', tvars)

	else:
		try:
			complete_rental = pmod.Rental.objects.get(id=request.urlparams[0])
			form = CheckRentalForm(initial ={
			'user': "",
			})
		except:
			pass
		form = "dfd"
		tvars = {
				'form': form,
		}
		return templater.render_to_response(request, 'return_rental.html', tvars)

class CheckRentalForm(forms.Form):
	user = forms.ModelChoiceField(queryset=pmod.User.objects.exclude(is_active=False), label="User", widget=forms.Select(attrs={'class':'form-control'}))
from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

# This view will display all users and then on a new page display all the current repairs for a given user

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shop')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/shop')

	#This form will display all users
	form = CheckRepairForm(initial ={
		'user': "",
	})
	
	if request.method == 'POST':
		form = CheckRepairForm(request.POST)
		if form.is_valid():
			#From here the page will redirect to show all the current repairs for the user picked
			complete = "/employee/customer_repairs/" + str(form.cleaned_data['user'].id)
			return HttpResponseRedirect(complete)
	
	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'check_repair.html', tvars)


class CheckRepairForm(forms.Form):
	user = forms.ModelChoiceField(queryset=pmod.User.objects.exclude(is_active=False), label="User", widget=forms.Select(attrs={'class':'form-control'}))
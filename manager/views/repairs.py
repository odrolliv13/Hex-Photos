from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.core.mail import send_mail

# This view displays the repairs

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/')
	
	if request.urlparams[0] == "email":
			completed = pmod.RepairStatus.objects.get(status="Completed")
			repairs = pmod.Repair.objects.filter(status=completed, paid=False)
			for i in repairs:
				message = i.user.first_name + " " + i.user.last_name + ":\r\n" + "The repair for the " + i.description + " with the  " + i.problem + " has been completed.\r\n Please return to the store to pick it up when you can.\r\nThank you!\r\n\r\nHexPhotos"
				send_mail('HexPhotos Repair Completed', message, 'no-reply@hexphotos.com', [i.user.email], fail_silently=True)
		

	'''Shows the list of catalog_products'''
	if request.urlparams[0] == "paid":
		Objects = pmod.Repair.objects.filter(paid=True)

	

	else:
		Objects = pmod.Repair.objects.filter(paid=False)

	tvars = {
		'Objects': Objects,
	}
	return templater.render_to_response(request, 'repairs.html', tvars)
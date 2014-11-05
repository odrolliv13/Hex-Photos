from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
import datetime
from django.core.mail import send_mail

# This view checks and grabs all the overdue rentals. It also allows an email to be sent to those customers

def process_request(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/')
	
	now = datetime.datetime.now()
	thirty_days = now - datetime.timedelta(days=30)
	sixty_days = now - datetime.timedelta(days=60)
	ninety_days = now - datetime.timedelta(days=90)

	thirty = pmod.Rental.objects.filter(return_date__isnull=True, expected_date__lt = now, expected_date__gte = thirty_days)
	sixty = pmod.Rental.objects.filter(return_date__isnull=True, expected_date__lt = thirty_days, expected_date__gte = sixty_days)
	ninety = pmod.Rental.objects.filter(return_date__isnull=True, expected_date__lt = sixty_days, expected_date__gte = ninety_days)
	ninetyplus = pmod.Rental.objects.filter(return_date__isnull=True, expected_date__lt = ninety_days)
	

	if request.urlparams[0] == "email":
		for i in thirty:
			message = i.user.first_name + " " + i.user.last_name + ":\r\n" + "The " + i.serialized.catalogID.name + " that you rented is overdue. It was due " + str(i.expected_date.strftime('%b %d, %Y')) + ".\r\n Please return it as soon as possible.\r\nThank you!\r\n\r\nHexPhotos"
			send_mail('HexPhotos Overdue Rental', message, 'no-reply@hexphotos.com', [i.user.email], fail_silently=True)
		for i in sixty:
			message = i.user.first_name + " " + i.user.last_name + ":\r\n" + "The " + i.serialized.catalogID.name + " that you rented is overdue. It was due " + str(i.expected_date.strftime('%b %d, %Y')) + ".\r\n Please return it as soon as possible.\r\nThank you!\r\n\r\nHexPhotos"
			send_mail('HexPhotos Overdue Rental', message, 'no-reply@hexphotos.com', [i.user.email], fail_silently=True)
		for i in ninety:
			message = i.user.first_name + " " + i.user.last_name + ":\r\n" + "The " + i.serialized.catalogID.name + " that you rented is overdue. It was due " + str(i.expected_date.strftime('%b %d, %Y')) + ".\r\n Please return it as soon as possible.\r\nThank you!\r\n\r\nHexPhotos"
			send_mail('HexPhotos Overdue Rental', message, 'no-reply@hexphotos.com', [i.user.email], fail_silently=True)
		for i in ninetyplus:
			message = i.user.first_name + " " + i.user.last_name + ":\r\n" + "The " + i.serialized.catalogID.name + " that you rented is overdue. It was due " + str(i.expected_date.strftime('%b %d, %Y')) + ".\r\n Please return it as soon as possible.\r\nThank you!\r\n\r\nHexPhotos"
			send_mail('HexPhotos Overdue Rental', message, 'no-reply@hexphotos.com', [i.user.email], fail_silently=True)

	tvars = {
		'thirty': thirty,
		'sixty': sixty,
		'ninety': ninety,
		'ninetyplus': ninetyplus
	}
	return templater.render_to_response(request, 'overdue_rentals.html', tvars)
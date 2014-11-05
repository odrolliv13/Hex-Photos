from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

def process_request(request):

	confirmed = False
	try:
		if request.urlparams[0]:
			user = pmod.User.objects.get(id = request.urlparams[0])
			if user.confirmedlink == request.urlparams[1]:
				now = datetime.datetime.now()
				if now.replace(tzinfo=None) < user.confirmeddate.replace(tzinfo=None):
					confirmed = True
					user.confirmed = True
					user.save()
	except:
		pass

	tvars = {
		'confirmed': confirmed,
	}
	return templater.render_to_response(request, 'confirmed.html', tvars)
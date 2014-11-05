from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater

def process_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shop/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/shop/')
	
	'''Shows the list of users'''
	if request.urlparams[0] == "deleted":
		Objects = pmod.User.objects.exclude(is_active=True)
		Object = pmod.User()
		ObjectID = 0
		Deleted = True
	elif request.urlparams[0] == "delete":
		user = pmod.User.objects.get(id=request.urlparams[1])
		user.is_active = False
		user.save()
		return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
		
	else:
		Objects = pmod.User.objects.exclude(is_active=False)
		Object = pmod.User()
		ObjectID = 0
		Deleted = False

	tvars = {
		'Objects': Objects,
		'Object': Object,
		'ObjectID': ObjectID,
		'Deleted': Deleted
	}
	return templater.render_to_response(request, 'users.html', tvars)
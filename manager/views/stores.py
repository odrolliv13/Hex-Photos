from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater

# This view displays the stores

def process_request(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/')
	
	'''Shows the list of stores'''
	if request.urlparams[0] == "deleted":
		Objects = pmod.Store.objects.exclude(active=True)
		Object = pmod.Store()
		ObjectID = 0
		Deleted = True
	elif request.urlparams[0] == "delete":
		store = pmod.Store.objects.get(id=request.urlparams[1])
		store.active = False
		store.save()
		return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
	else:
		Objects = pmod.Store.objects.exclude(active=False)
		Object = pmod.Store()
		ObjectID = 0
		Deleted = False

	tvars = {
		'Objects': Objects,
		'Object': Object,
		'ObjectID': ObjectID,
		'Deleted': Deleted
	}
	return templater.render_to_response(request, 'stores.html', tvars)
from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater

# This view displays the categories

def process_request(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/manager/login')

	if request.user.is_staff == False:
		return HttpResponseRedirect('/manager/')
	
	'''Shows the list of stores'''
	if request.urlparams[0] == "deleted":
		Objects = pmod.Category.objects.exclude(is_active=True)
		Object = pmod.Category()
		ObjectID = 0
		Deleted = True
	if request.urlparams[0] == "delete":
		category = pmod.Category.objects.get(id=request.urlparams[1])
		category.is_active = False
		category.save()
		return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
	else:
		Objects = pmod.Category.objects.exclude(is_active=False)
		Object = pmod.Category()
		ObjectID = 0
		Deleted = False

	tvars = {
		'Objects': Objects,
		'Object': Object,
		'ObjectID': ObjectID,
		'Deleted': Deleted
	}
	return templater.render_to_response(request, 'categories.html', tvars)
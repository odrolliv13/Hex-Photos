from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import logout



def process_request(request):
	'''py that logs out a user when requested and redirects to index'''
	
	logout(request)
	return HttpResponseRedirect('/shop/')
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import logout

def process_request(request):
	logout(request)
	return HttpResponseRedirect('/manager/index/')
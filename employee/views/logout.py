from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import logout

# This view logs a user out

def process_request(request):
	logout(request)
	return HttpResponseRedirect('/shop/')
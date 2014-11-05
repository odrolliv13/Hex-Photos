from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from django.db.models import Q
from . import templater

def process_request(request):
	'''py that handles the query of items'''

	if request.method == 'GET':
		query = request.GET.get('search')
	if query is None:
		search = False
		Objects = ""
		results = False
	else:
		search = True
		query = query.lower()
		print(query)
		
		#returns the objects that match the query
		Objects = pmod.CatalogProduct.objects.filter(Q(lname__contains=query) | Q(ldescription__contains=query) | Q(lbrand__contains=query), is_active=True)
		count = 0
		for number in Objects:
			count += 1
		if count > 0:
			results = True
		else:
			results = False

		
	tvars = {
		'search': search,
		'Objects': Objects,
		'results': results,
	}
	return templater.render_to_response(request, 'search.html', tvars)
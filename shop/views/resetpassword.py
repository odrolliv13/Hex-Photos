from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime

def process_request(request):
	'''this py handles the reset password functionality'''
	

	if request.urlparams[0]:
		user = pmod.User.objects.get(id = request.urlparams[0])
		if user.resetlink == request.urlparams[1]:
			now = datetime.datetime.now()			
			if now.replace(tzinfo=None) < user.resetdate.replace(tzinfo=None):
				form = PasswordForm(initial ={
					'newpassword': "",
					'retypepassword': "",
					})
				
				#when form is submited the new user's password is saved to their db account
				if request.method == 'POST':
					form = PasswordForm(request.POST, request=request)
					if form.is_valid():
						user = pmod.User.objects.get(id = request.urlparams[0])
						user.set_password(form.cleaned_data['newpassword'])
						user.save()
						return HttpResponseRedirect('/shop/')
			else:
				return HttpResponseRedirect('/shop/')
		else:
			return HttpResponseRedirect('/shop/')
	else:
		return HttpResponseRedirect('/shop/account/general')

	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'resetpassword.html', tvars)

class PasswordForm(forms.Form):
	newpassword = forms.CharField(required=False, label='New Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	retypepassword = forms.CharField(required=False, label='Confirm New Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(PasswordForm, self).__init__(*args, **kwargs)

	def clean(self):
		if self.cleaned_data['newpassword'] != self.cleaned_data['retypepassword']:
			raise forms.ValidationError("The passwords do not match.")
		return self.cleaned_data
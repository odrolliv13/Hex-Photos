from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from manager import models as pmod
from . import templater
from django.core.mail import send_mail, EmailMultiAlternatives
import decimal, datetime, string, random

def process_request(request):
	'''py that handles the functionality of creating a new account'''
	if request.user.is_authenticated():
		return HttpResponseRedirect('/shop/')

	form = UserForm(initial ={
	'username': "",
	'email': "",
	'password': "",
	'retypepassword': "",
	})

	#when user submits form, a new user is created with the information provided
	#a random link is generated and stored in the user's db. 
	if request.method == 'POST':
		form = UserForm(request.POST, request=request)
		if form.is_valid():
			user = pmod.User()
			user.email = form.cleaned_data['email']
			user.username = form.cleaned_data['username']
			user.set_password(form.cleaned_data['password'])
			user.confirmed = False
			link = ''.join(random.choice(string.ascii_uppercase) for i in range(15))
			date = datetime.datetime.now() + datetime.timedelta(hours=2)
			user.confirmedlink = link
			user.confirmeddate = date
			user.save()

			#this adds to the new user this credit card information for testing purposes. 
			validcard = pmod.UserBilling()
			validcard.user = user
			validcard.name = "Cosmo Limesandal"
			visa = pmod.CardType.objects.get(name = "Visa")
			validcard.cardtype = visa
			validcard.number = "4732817300654"
			validcard.security = "411"
			validcard.expmonth = 10
			validcard.expyear = 14
			validcard.save()

			#the following lines generate an emial that is sent to the customer to confirm account
			html = "<html><body></body>Please click <a href=\"http://www.djuvo.com/shop/confirmed/" + str(user.id) +"/" + str(user.confirmedlink) + "\">here</a> to verify your account.<br>Thank you!<br>HexPhotos</html>"
			message = "/shop/confirmed/" + str(user.id) +"/" + str(user.confirmedlink)
			message = html

			msg = EmailMultiAlternatives('HexPhotos Confirmation Email', message, 'hexphotos.byu@gmail.com', [user.email])
			msg.attach_alternative(html, "text/html")
			msg.send()

			#once the account is created, the user is being logged in
			loginuser = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
			login(request, loginuser)
			redirect = request.META.get("HTTP_REFERER")
			return HttpResponse('<script> window.location.href="' + redirect +'" </script>')

	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'new_account.html', tvars)

class UserForm(forms.Form):
	username = forms.CharField(required=False, label='Username', widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(required=False, label='Email', widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(required=False, label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	retypepassword = forms.CharField(required=False, label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))


	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(UserForm, self).__init__(*args, **kwargs)

	def clean(self):
		allUsers = pmod.User.objects.all()
		for u in allUsers:
			if self.cleaned_data['email'] == u.email:
				raise forms.ValidationError("That email is already in use.")
		if self.cleaned_data['password'] == "":
			raise forms.ValidationError("You must enter a password.")
		if self.cleaned_data['password'] != self.cleaned_data['retypepassword']:
			raise forms.ValidationError("The passwords do not match.")
		return self.cleaned_data

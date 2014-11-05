from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater
from django.conf import settings
import decimal, datetime, string, random
from django.core.mail import send_mail, EmailMultiAlternatives

def process_request(request):
	'''this py handles the forget password functionality. Sends an email to recover password'''

	#makes sure the user is already logged in
	if request.user.is_authenticated():
		return HttpResponseRedirect('/shop/account')

	form = RequestForm(initial ={
		'username': "",
		})
	
	#generates form that takes the customer's username and then, sends a link to thier email with a
	#link to reset password			
	if request.method == 'POST':
		form = RequestForm(request.POST, request=request)
		if form.is_valid():
			user = pmod.User.objects.get(username=form.cleaned_data['username'])
			link = ''.join(random.choice(string.ascii_uppercase) for i in range(15))
			date = datetime.datetime.now() + datetime.timedelta(hours=2)
			user.resetlink = link
			user.resetdate = date
			user.save()
			html = "<html><body></body>Please click <a href=\"http://www.hexphotos.com/shop/resetpassword/" + str(user.id) +"/" + str(user.resetlink) + "\">here</a> to reset your password. This reset link will expire in 2 hours.<br>Thank you!<br>HexPhotos</html>"
			message = "/shop/resetpassword/" + str(user.id) +"/" + str(user.resetlink)
			message = html

			msg = EmailMultiAlternatives('HexPhotos Password Reset', message, 'no-reply@hexphotos.com', [user.email])
			msg.attach_alternative(html, "text/html")
			msg.send()

			return HttpResponseRedirect('/shop/emailsent')

	tvars = {
		'form': form,
	}
	return templater.render_to_response(request, 'forgotpassword.html', tvars)

class RequestForm(forms.Form):
	username = forms.CharField(required=False, label='Username', widget=forms.TextInput(attrs={'class':'form-control'}))

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(RequestForm, self).__init__(*args, **kwargs)

	#function that raises error if username does not match any account	
	def clean(self):
		try:
			user = pmod.User.objects.get(username=self.cleaned_data['username'])
		except:
			raise forms.ValidationError("That email does not correspond to a user.")
		return self.cleaned_data
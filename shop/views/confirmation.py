from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from manager import models as pmod
from . import templater
import decimal, datetime, string, random
from django.core.mail import send_mail, EmailMultiAlternatives

def process_request(request):
	'''this py handles the functionality to resend an account confirmation email'''
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shop/')

	link = ''.join(random.choice(string.ascii_uppercase) for i in range(15))
	date = datetime.datetime.now() + datetime.timedelta(hours=2)
	request.user.confirmedlink = link
	request.user.confiremddate = date
	request.user.save()

	#here the email format is generated with the link to return to the app
	html = "<html><body></body>Please click <a href=\"http://www.djuvo.com/shop/confirmed/" + str(request.user.id) +"/" + str(request.user.confirmedlink) + "\">here</a> to verify your account.<br>Thank you!<br>HexPhotos</html>"
	message = "/shop/confirmed/" + str(request.user.id) +"/" + str(request.user.confirmedlink)
	message = html

	msg = EmailMultiAlternatives('HexPhotos Confirmation Email', message, 'hexphotos.byu@gmail.com', [request.user.email])
	msg.attach_alternative(html, "text/html")
	msg.send()

	tvars = {
	}
	return templater.render_to_response(request, 'confirmation.html', tvars)

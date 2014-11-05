from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater



def process_request(request):
	'''this py handles the customer's account information, including ability to reset password an
	cancel an account.'''
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shop/account')
	
	transactions = ""
	transactionstopack = ""
	repairs = ""
	rentals = ""
	form = ""
	page = ""
	display = ""
	#this if statement handles the ability to change password
	if request.urlparams[0] == "security":
		page = "security"
		form = PasswordForm(initial ={
		'oldpassword': "",
		'newpassword': "",
		'retypepassword': "",
		})
		if request.method == 'POST':
			form = PasswordForm(request.POST, request=request)
			if form.is_valid():
				user = pmod.User.objects.get(username = request.user.username)
				user.set_password(form.cleaned_data['newpassword'])
				user.save()
				return HttpResponseRedirect('/shop/account/general')

	#when hitting this billing if statement, the user's billing information is pulled
	#for display and ability to delete.			
	elif request.urlparams[0] == "billing":
		user = pmod.User.objects.get(username = request.user.username)
		display = pmod.UserBilling.objects.filter(user = user)
		page = "billing"
		#deletes credit card
		if request.urlparams[1] == "delete":
			deletebilling = pmod.UserBilling.objects.get(id = request.urlparams[2])
			deletebilling.delete()
			return HttpResponseRedirect('/shop/account/billing')
	



	#when hitting this if statement, the user's shipping info is pulled
	elif request.urlparams[0] == "shipping":
		user = pmod.User.objects.get(username = request.user.username)
		display = pmod.UserShipping.objects.filter(user = user)
		page = "shipping"
		#if statemeent with functionality to delete a shipping address
		if request.urlparams[1] == "delete":
			deleteshipping = pmod.UserShipping.objects.get(id = request.urlparams[2])
			deleteshipping.delete()
			return HttpResponseRedirect('/shop/account/shipping')

	#when hitting this if statement, if there are any repairs in process, it will pull
	#all of them.		
	elif request.urlparams[0] == "repairs":
		user = pmod.User.objects.get(username = request.user.username)
		display = pmod.Repair.objects.filter(user = user, date_returned__isnull=True)
		page = "repairs"

	#when hitting this if statement, if there are any rentals checked out, it will pull
	#them all.		
	elif request.urlparams[0] == "rentals":
		user = pmod.User.objects.get(username = request.user.username)
		display = pmod.Rental.objects.filter(user = user, return_date__isnull=True)
		page = "rentals"

	#thi if statement handles the orders history of the customer. 	
	elif request.urlparams[0] == "orders":
		user = pmod.User.objects.get(username = request.user.username)
		transactions = pmod.Transaction.objects.filter(buyer = user).order_by('-date')
		transactionstopack = []
		rentals = []
		repairs = []
		for t in transactions:
			temp = pmod.TransactionToPack.objects.filter(transaction = t)
			for e in temp:
				transactionstopack.append(e)
			temp = pmod.RentalTransaction.objects.filter(transaction = t)
			for e in temp:
				rentals.append(e)
			temp = pmod.RepairTransaction.objects.filter(transaction = t)
			for e in temp:
				repairs.append(e)

		page = "orders"

	#this if statement handles account's cancelation. It actually just sets it to inactive 	
	elif request.urlparams[0] == "cancellation":
		page = "cancellation"
		form = CancelForm(initial ={
		'password': "",
		})
		if request.method == 'POST':
			form = CancelForm(request.POST)
			if form.is_valid():
				user = pmod.User.objects.get(username = request.user.username)
				if user.check_password(form.cleaned_data['password']) == True:
					user.is_active = False
					user.save()
					return HttpResponseRedirect('/shop/logout')


	#this if stement displays all general information of the customer				
	else:
		page = "general"
		display = pmod.User.objects.get(username = request.user.username)
		if request.urlparams[1] == "edit":
			page = "generaledit"
			user = pmod.User.objects.get(username = request.user.username)
			form = UserForm(initial ={
			'username': user.username,
			'email': user.email,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'street': user.street,
			'city': user.city,
			'state': user.state,
			'zipcode': user.zipcode,
			'phone': user.phone,
			})
			if request.method == 'POST':
				form = UserForm(request.POST, request=request)
				if form.is_valid():
					user.email = form.cleaned_data['email']
					user.username = form.cleaned_data['username']
					user.first_name = form.cleaned_data['first_name']
					user.last_name = form.cleaned_data['last_name']
					user.street = form.cleaned_data['street']
					user.city = form.cleaned_data['city']
					user.state = form.cleaned_data['state']
					user.zipcode = form.cleaned_data['zipcode']
					user.phone = form.cleaned_data['phone']
					user.save()
					return HttpResponseRedirect('/shop/account/general/')

	shippingobject = pmod.UserShipping()
	billingobject = pmod.UserShipping()
	tvars = {
		'form': form,
		'page': page,
		'display': display,
		'shippingobject': shippingobject,
		'billingobject': billingobject,
		'transactions': transactions,
		'transactionstopack': transactionstopack,
		'repairs': repairs,
		'rentals': rentals,
	}
	return templater.render_to_response(request, 'account.html', tvars)

#form for canceling account
class CancelForm(forms.Form):
	password = forms.CharField(required=False, label='Current Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	
#form for changing password
class PasswordForm(forms.Form):
	oldpassword = forms.CharField(required=False, label='Current Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	newpassword = forms.CharField(required=False, label='New Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	retypepassword = forms.CharField(required=False, label='Confirm New Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(PasswordForm, self).__init__(*args, **kwargs)

	#function that checks if the current password matches and the new and confirm as well	
	def clean(self):
		if self.request.user.check_password(self.cleaned_data['oldpassword']) != True:
			raise forms.ValidationError("That is not the current password.")
		if self.cleaned_data['newpassword'] != self.cleaned_data['retypepassword']:
			raise forms.ValidationError("The passwords do not match.")
		return self.cleaned_data

#form to create general info of customer
class UserForm(forms.Form):
	username = forms.CharField(required=False, label='Username', widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(required=False, label='Email', widget=forms.TextInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(required=False, label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(required=False, label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}))
	street = forms.CharField(required=False, label='Street', widget=forms.TextInput(attrs={'class':'form-control'}))
	city  = forms.CharField(required=False, label='City', widget=forms.TextInput(attrs={'class':'form-control'}))
	state  = forms.CharField(required=False, label='State', widget=forms.TextInput(attrs={'class':'form-control'}))
	zipcode  = forms.CharField(required=False, label='Zipcode', widget=forms.TextInput(attrs={'class':'form-control'}))
	phone  = forms.CharField(required=False, label='Phone', widget=forms.TextInput(attrs={'class':'form-control'}))

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(UserForm, self).__init__(*args, **kwargs)

	def clean(self):
		allUsers = pmod.User.objects.all()
		for u in allUsers:
			if self.cleaned_data['email'] == u.email:
				if self.cleaned_data['email'] == self.request.user.email:
					pass
				else:
					raise forms.ValidationError("That email is already in use.")
			if self.cleaned_data['username'] == u.username:
				if self.cleaned_data['username'] == self.request.user.username:
					pass
				else:
					raise forms.ValidationError("That username is already in use.")	
		return self.cleaned_data
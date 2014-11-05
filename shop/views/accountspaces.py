from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manager import models as pmod
from . import templater

def process_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/shop/login')
    form = ""
    page = ""
    display = ""
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


    elif request.urlparams[0] == "billing":
        user = pmod.User.objects.get(username = request.user.username)
        display = pmod.UserBilling.objects.filter(user = user)
        page = "billing"

        if request.urlparams[1] == "delete":
            deletebilling = pmod.UserBilling.objects.get(id = request.urlparams[2])
            deletebilling.delete()
            return HttpResponseRedirect('/shop/account/billing')
    



    
    elif request.urlparams[0] == "shipping":
        user = pmod.User.objects.get(username = request.user.username)
        display = pmod.UserShipping.objects.filter(user = user)
        page = "shipping"

        if request.urlparams[1] == "delete":
            deleteshipping = pmod.UserShipping.objects.get(id = request.urlparams[2])
            deleteshipping.delete()
            return HttpResponseRedirect('/shop/account/shipping')

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

    else:
        page = "general"
        display = pmod.User.objects.get(username = request.user.username)
        if request.urlparams[1] == "edit":
            page = "generaledit"
            user = pmod.User.objects.get(username = request.user.username)
            form = UserForm(initial ={
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
                    user.username = form.cleaned_data['email']
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
    }
    return templater.render_to_response(request, 'account.html', tvars)

class CancelForm(forms.Form):
    password = forms.CharField(required=False, label='Current Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    

class PasswordForm(forms.Form):
    oldpassword = forms.CharField(required=False, label='Current Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    newpassword = forms.CharField(required=False, label='New Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    retypepassword = forms.CharField(required=False, label='Confirm New Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request.user.check_password(self.cleaned_data['oldpassword']) != True:
            raise forms.ValidationError("That is not the current password.")
        if self.cleaned_data['newpassword'] != self.cleaned_data['retypepassword']:
            raise forms.ValidationError("The passwords do not match.")
        return self.cleaned_data

class UserForm(forms.Form):
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
        return self.cleaned_data
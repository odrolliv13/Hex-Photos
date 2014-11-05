import requests
import decimal

class payment():
	''' This class connects to a payment gateway to check credit cards '''
	
	def setVariables(self, userbilling, subtotal, taxRate):
		''' This function sets the variables '''
		self.userbilling = userbilling
		self.subtotal = subtotal
		self.taxRate = taxRate

	def check(self):
		''' This function returns a boolean on if the payment was valid '''
		API_URL = 'http://dithers.cs.byu.edu/iscore/api/v1/charges'
		API_KEY = '3e311af5eb2ef6764019d5d6a877b11e'
		
		r = requests.post(API_URL, data={
			'apiKey': API_KEY,
			'currency': 'usd',
			'amount': str(self.subtotal + (self.subtotal * self.taxRate)),
			'type': str(self.userbilling.cardtype.name),
			'number': str(self.userbilling.number),
			'exp_month': self.userbilling.expmonth,
			'exp_year': self.userbilling.expyear,
			'cvc': self.userbilling.security,
			'name': str(self.userbilling.name),
			'description': 'Charge for ' + str(self.userbilling.user.username),
		})
		resp = r.json()
		if "error" in resp:
			return False
		else:
			return True
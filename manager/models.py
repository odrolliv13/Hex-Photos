from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Info():
	''' This class is used to pass info to the pages'''
	def __init__(self, key, value, edit):
		self.key = key
		self.value = value
		self.edit = edit

class User(AbstractUser):
	''' This is the user class'''
	User._meta.get_field('email')._unique = True
	street = models.TextField(blank=True, null=True)
	city =  models.TextField(blank=True, null=True)
	state =  models.TextField(blank=True, null=True)
	zipcode =  models.TextField(blank=True, null=True)
	country =  models.TextField(blank=True, null=True)
	phone =  models.TextField(blank=True, null=True)
	salary = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	hourlypay = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	commissionRate = models.DecimalField(blank=True, null=True, decimal_places=3, max_digits=4)
	resetlink = models.TextField(blank=True, null=True)
	resetdate = models.DateTimeField(blank=True, null=True)
	confirmed =  models.NullBooleanField()
	confirmedlink = models.TextField(blank=True, null=True)
	confirmeddate = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.username + " | " + self.first_name + " " + self.last_name

	
	def info(self):
		''' This function displays most user info for use in the manager app '''
		info = []
		info.append(Info("Username", self.username, False))
		info.append(Info("Email", self.email, False))
		info.append(Info("First Name", self.first_name, True))
		info.append(Info("Last Name", self.last_name, True))
		info.append(Info("Street", self.street, True))
		info.append(Info("City", self.city, True))
		info.append(Info("State", self.state, True))
		info.append(Info("Zipcode", self.zipcode, True))
		info.append(Info("Phone", self.phone, True))
		info.append(Info("Staff", self.is_staff, True))
		info.append(Info("Admin", self.is_superuser, True))
		return info

	
	def customer(self):
		''' This function displays user info meant for customers in the shop app '''
		info = []
		info.append(Info("Username", self.username, False))
		info.append(Info("Email", self.email, False))
		info.append(Info("First Name", self.first_name, True))
		info.append(Info("Last Name", self.last_name, True))
		info.append(Info("Street", self.street, True))
		info.append(Info("City", self.city, True))
		info.append(Info("State", self.state, True))
		info.append(Info("Zipcode", self.zipcode, True))
		info.append(Info("Phone", self.phone, True))
		return info		


class UserShipping(models.Model):
	''' This class holds shipping information for a customer '''
	user = models.ForeignKey(User)
	name = models.TextField(blank=True, null=True)
	street = models.TextField(blank=True, null=True)
	city =  models.TextField(blank=True, null=True)
	state =  models.TextField(blank=True, null=True)
	zipcode =  models.TextField(blank=True, null=True)

	def __str__(self):
		return self.user.username + ": " + self.name

	def customer(self):
		info = []
		info.append(Info("Name", self.name, False))
		info.append(Info("Street", self.street, True))
		info.append(Info("City", self.city, True))
		info.append(Info("State", self.state, True))
		info.append(Info("Zipcode", self.zipcode, True))
		return info	


class CardType(models.Model):
	''' This class determines which types of cards the company accepts - Not editable through manager app should be added by admin '''
	name = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name


class UserBilling(models.Model):
	''' This class holds billing information for a customer '''
	user = models.ForeignKey(User)
	name = models.TextField(blank=True, null=True)
	cardtype = models.ForeignKey(CardType)
	number = models.TextField(blank=True, null=True)
	security = models.TextField(blank=True, null=True)
	street = models.TextField(blank=True, null=True)
	city =  models.TextField(blank=True, null=True)
	state =  models.TextField(blank=True, null=True)
	zipcode =  models.TextField(blank=True, null=True)
	expmonth = models.PositiveIntegerField()
	expyear = models.PositiveIntegerField()


class ShippingOption(models.Model):
	''' This class holds shipping options for the customer '''
	daystoarrive = models.PositiveIntegerField()
	price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)


class TransactionType(models.Model):
	''' This holds the different transaction types availabe - Not editable in manager app because some code depends on certain naming conventions '''
	transactiontype = models.TextField(blank=True, null=True)


class Transaction(models.Model):
	''' This class holds a transaction '''
	buyer = models.ForeignKey(User)
	seller = models.ForeignKey(User, limit_choices_to={'is_staff': True}, related_name="trans_seller")
	transactiontype = models.ForeignKey(TransactionType)
	shipping = models.ForeignKey(UserShipping, blank=True, null=True)
	billing = models.ForeignKey(UserBilling)
	shippingoption = models.ForeignKey(ShippingOption, blank=True, null=True)
	subtotal = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	taxAmount = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	date = models.DateTimeField(blank=True, null=True)
	commissionNeeded = models.NullBooleanField()
	packed = models.NullBooleanField()

	def __str__(self):
		return self.buyer.username + " | " + self.seller.username + " | "


class Commission(models.Model):
	''' This class holds commission from a transaction '''
	transaction = models.ForeignKey(Transaction)
	seller = models.ForeignKey(User, limit_choices_to={'is_staff': True}, related_name="trans_seller_commission")
	amount = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	paid = models.NullBooleanField()

class TaxRates(models.Model):
	''' This holds tax rates - Should be managed by admin '''
	state =  models.TextField(blank=True, null=True)
	taxRate = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=3)

class JournalEntry(models.Model):
	'''This class records a journal entry '''
	transaction = models.ForeignKey(Transaction)
	note =  models.CharField(max_length=1000, blank=True, null=True)

class Subledger(models.Model):
	''' This class holds the different types of subledgers - Should be managed by admin because of dependencies '''
	type =  models.CharField(max_length=1000, blank=True, null=True)

	def __str__(self):
		return self.type

class DebitCredit(models.Model):
	''' This class models a debit or a credit to a particular subledger '''
	journalentry = models.ForeignKey(JournalEntry)
	subledger = models.ForeignKey(Subledger)
	isDebit = models.NullBooleanField()
	amount = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)

	def __str__(self):
		return self.subledger.type + ": " + str(self.amount)

class GeneralLedger(models.Model):
	date = models.DateTimeField(auto_now_add=True, blank=True)
	subledger = models.ForeignKey(Subledger)
	isDebit = models.NullBooleanField()
	amount = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)


class Store(models.Model):
	'''A store object'''
	locationName = models.TextField(blank=True, null=True)
	manager = models.ForeignKey(User, limit_choices_to={'is_staff': True}, related_name="store_manager", blank=True, null=True)
	street = models.TextField(blank=True, null=True)
	city  = models.TextField(blank=True, null=True)
	state  = models.TextField(blank=True, null=True)
	zipcode  = models.TextField(blank=True, null=True)
	phone  = models.TextField(blank=True, null=True)
	active = models.NullBooleanField()

	def __str__(self):
		return self.locationName

	def info(self):
		info = []
		info.append(Info("Location Name", self.locationName, False))
		info.append(Info("Street", self.street, True))
		info.append(Info("City", self.city, True))
		info.append(Info("State", self.state, True))
		info.append(Info("Zipcode", self.zipcode, True))
		info.append(Info("Phone", self.phone, True))
		return info

class Category(models.Model):
	''' This class defines the different categories - Should be managed by the admin because of dependencies '''
	name = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	imagePath = models.CharField(max_length=100, blank=True, null=True)
	url = models.CharField(max_length=50, blank=True, null=True)
	#url contains where 
	is_active = models.NullBooleanField()
	queryURL = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.name

	def info(self):
		info = []
		info.append(Info("Name", self.name, False))
		info.append(Info("Description", self.description, False))
		return info


class InventoryType(models.Model):
	''' This class defines whether the CatalogProduct is Stocked or Serialized - Should be managed by Admin '''
	name = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name

class CatalogProduct(models.Model):
	''' This class holds a catalog product. CatalogProducts are the different types of products the company can stock '''
	catalogID = models.TextField(blank=True, null=True)
	inventorytype = models.ForeignKey(InventoryType)
	name = models.TextField(blank=True, null=True)
	lname = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	ldescription = models.TextField(blank=True, null=True)
	brand = models.TextField(blank=True, null=True)
	lbrand = models.TextField(blank=True, null=True)
	category = models.ForeignKey(Category)
	imagePath = models.CharField(max_length=100, blank=True, null=True)
	#imagePath stores the path to the image. Pictures can not be uploaded through the manager app. This is because of the need to properly format pictures before uploading and displaying them on the server
	price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	rentalPrice = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	replacementPrice = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	is_active = models.NullBooleanField()

	

	def info(self):
		info = []
		info.append(Info("CatalogID", self.catalogID, False))
		info.append(Info("Name", self.name, False))
		info.append(Info("Description", self.description, False))
		info.append(Info("Brand", self.brand, False))
		info.append(Info("Price", self.price, False))
		info.append(Info("Rental Price", self.rentalPrice, False))
		info.append(Info("Replacement Price", self.replacementPrice, False))
		return info

	def __str__(self):
		return self.catalogID + ": " + self.name 


class TransactionToPack(models.Model):
	''' This class holds what is needed to pack for a transaction ordered from the online store. '''
	transaction = models.ForeignKey(Transaction)
	catalog_product = models.ForeignKey(CatalogProduct)
	quantity = models.PositiveIntegerField()
	packed = models.NullBooleanField()


class StockedProduct(models.Model):
	''' This class represents an actual product of the CatalogProduct '''
	catalogID = models.ForeignKey(CatalogProduct)
	amount = models.PositiveIntegerField()
	cost = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	store = models.ForeignKey(Store)
	is_active = models.NullBooleanField()

	def __str__(self):
		return self.catalogID.catalogID + ": " + self.catalogID.name + " - "  + self.store.locationName	+ " | " + str(self.amount)

	def info(self):
		info = []
		info.append(Info("Amount", self.amount, False))
		info.append(Info("Cost", self.cost, False))
		return info

class SerializedProduct(models.Model):
	''' This class represents a single actual serialized product off the CatalogProduct '''
	catalogID = models.ForeignKey(CatalogProduct)
	serialNumber = models.TextField(blank=True, null=True)
	datePurchased = models.DateTimeField(blank=True, null=True)
	cost = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	store = models.ForeignKey(Store)
	is_rental = models.NullBooleanField()
	is_available = models.NullBooleanField()
	is_new = models.NullBooleanField()
	is_active = models.NullBooleanField()

	def info(self):
		info = []
		info.append(Info("Serial Number", self.serialNumber, False))
		info.append(Info("Cost", self.cost, False))
		info.append(Info("Rental", self.is_rental, False))
		info.append(Info("Available", self.is_available, False))
		info.append(Info("New", self.is_new, False))
		info.append(Info("Date Purchased", self.datePurchased, False))
		return info

	def __str__(self):
		return self.catalogID.catalogID + ": " + self.catalogID.name + " - " + self.store.locationName + " | " + self.serialNumber 	+ " | " + str(self.datePurchased)


class Rental(models.Model):
	''' This class represents a rental '''
	user = models.ForeignKey(User)
	serialized = models.ForeignKey(SerializedProduct)
	daily_rate = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	checkout_date = models.DateTimeField(blank=True, null=True)
	checkout_condition = models.CharField(max_length=100, blank=True, null=True)
	days_to_rent = models.PositiveIntegerField()
	expected_date = models.DateTimeField(blank=True, null=True)
	return_date = models.DateTimeField(blank=True, null=True)
	return_condition = models.CharField(max_length=100, blank=True, null=True)
	before_fees = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	late_fees = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	damage_fees = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	damage_note = models.CharField(max_length=100, blank=True, null=True)
	paid = models.NullBooleanField()
	
	def __str__(self):
		return self.user.username + " | " + self.serialized.catalogID.name

class RepairStatus(models.Model):
	''' This class holds the statuses of In Progress and Completed so users can check the status of their repair'''
	status = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.status
	
class Repair(models.Model):
	''' This class represents a repair '''
	user = models.ForeignKey(User)
	serial_number = models.CharField(max_length=100, blank=True, null=True)
	description = models.CharField(max_length=100, blank=True, null=True)
	date_received = models.DateTimeField(blank=True, null=True)
	problem = models.CharField(max_length=100, blank=True, null=True)
	status = models.ForeignKey(RepairStatus)
	estimate = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	additional_cost = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	# additional_cost represents how much more should be added to the estimate for the customer
	cost = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	#cost represents the actual cost of the repair. Field is used for accounting purposes.
	costs_note = models.CharField(max_length=1000, blank=True, null=True)
	total_charged = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	date_returned = models.DateTimeField(blank=True, null=True)
	paid = models.NullBooleanField()
	
	def __str__(self):
		return self.user.username + " | " + self.description

class StockedTransaction(models.Model):
	''' This class connects a stocked item to a transaction '''
	transaction = models.ForeignKey(Transaction)
	stocked = models.ForeignKey(StockedProduct)
	amount = models.PositiveIntegerField()

class SerializedTransaction(models.Model):
	''' This class connects a serialized item to a transaction '''
	transaction = models.ForeignKey(Transaction)
	serialized = models.ForeignKey(SerializedProduct)

class RepairTransaction(models.Model):
	''' This class connects a repair to a transaction '''
	transaction = models.ForeignKey(Transaction)
	repair = models.ForeignKey(Repair)

class RentalTransaction(models.Model):
	''' This class connects a rental to a transaction '''
	transaction = models.ForeignKey(Transaction)
	rental = models.ForeignKey(Rental)
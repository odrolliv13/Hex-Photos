from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Info():
	def __init__(self, key, value, edit):
		self.key = key
		self.value = value
		self.edit = edit



class Store(models.Model):
	'''A store object'''
	locationName = models.CharField(max_length=20, blank=True, null=True)
	street = models.CharField(max_length=20, blank=True, null=True)
	city  = models.CharField(max_length=20, blank=True, null=True)
	state  = models.CharField(max_length=20, blank=True, null=True)
	zipcode  = models.CharField(max_length=20, blank=True, null=True)
	phone  = models.CharField(max_length=20, blank=True, null=True)
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

class CatalogProduct(models.Model):
	catalogID = models.CharField(max_length=20, blank=True, null=True)
	name = models.CharField(max_length=20, blank=True, null=True)
	lname = models.CharField(max_length=20, blank=True, null=True)
	description = models.CharField(max_length=20, blank=True, null=True)
	ldescription = models.CharField(max_length=20, blank=True, null=True)
	brand = models.CharField(max_length=20, blank=True, null=True)
	lbrand = models.CharField(max_length=20, blank=True, null=True)
	category = models.CharField(max_length=20, blank=True, null=True)
	commissionRate = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=3)
	rentalPrice = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	replacementPrice = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	is_active = models.NullBooleanField()

	def info(self):
		info = []
		info.append(Info("CatalogID", self.catalogID, False))
		info.append(Info("Name", self.name, False))
		info.append(Info("Description", self.description, False))
		info.append(Info("Brand", self.brand, False))
		info.append(Info("Category", self.category, False))
		info.append(Info("Commission Rate", self.commissionRate, False))
		info.append(Info("Rental Price", self.rentalPrice, False))
		info.append(Info("Replacement Price", self.replacementPrice, False))
		return info

	def __str__(self):
		return self.catalogID + ": " + self.name 

class StockedProduct(models.Model):
	catalogID = models.ForeignKey(CatalogProduct)
	amount = models.PositiveIntegerField()
	cost = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	store = models.ForeignKey(Store)
	is_active = models.NullBooleanField()

	def __str__(self):
		return self.catalogID.catalogID + ": " + self.catalogID.name + " - "  + self.store.locationName	

	def info(self):
		info = []
		info.append(Info("Amount", self.amount, False))
		info.append(Info("Cost", self.cost, False))
		return info

class SerializedProduct(models.Model):
	catalogID = models.ForeignKey(CatalogProduct)
	serialNumber = models.CharField(max_length=20, blank=True, null=True)
	datePurchased = models.DateField()
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
		return self.catalogID.catalogID + ": " + self.catalogID.name + " - " + self.store.locationName + " | " + self.serialNumber 	
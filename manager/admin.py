from django.db import models
from django.contrib import admin
from .models import *

# register any models here
admin.site.register(Store)
admin.site.register(User)
admin.site.register(CatalogProduct)
admin.site.register(StockedProduct)
admin.site.register(SerializedProduct)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(UserShipping)
admin.site.register(CardType)
admin.site.register(UserBilling)
admin.site.register(ShippingOption)
admin.site.register(TransactionType)
admin.site.register(TaxRates)
admin.site.register(JournalEntry)
admin.site.register(Subledger)
admin.site.register(DebitCredit)
admin.site.register(GeneralLedger)
admin.site.register(StockedTransaction)
admin.site.register(SerializedTransaction)
admin.site.register(Rental)
admin.site.register(RepairStatus)
admin.site.register(Repair)
admin.site.register(TransactionToPack)
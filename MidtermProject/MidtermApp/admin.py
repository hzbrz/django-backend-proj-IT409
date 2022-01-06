from django.contrib import admin

# Register your models here.
from .models import Customer, Address, Account, Transaction

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Account)
admin.site.register(Transaction)

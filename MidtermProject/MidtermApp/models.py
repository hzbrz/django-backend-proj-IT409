from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=25, null=False)
    last_name = models.CharField(max_length=25, null=False)
    ssn = models.CharField(max_length=25, null=False)
    customer_since = models.DateField(auto_now_add=True)
    preferred_customer = models.BooleanField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        ordering = ['first_name']  # asc

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    street = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=25, null=False)
    state = models.CharField(max_length=10, null=False)
    zip = models.CharField(max_length=11, null=False)

    def __str__(self):  # String representation
        return self.street + ' ' + self.city + ' ' + self.state + ' ' + self.zip

    class Meta:
        ordering = ['zip']  # asc

class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, null=False)
    account_type = models.CharField(max_length=15, null=False)
    balance = models.FloatField(null=False, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return str(self.id) + ' customer no.' + str(self.customer)

    class Meta:
        order_with_respect_to = 'customer'


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    action = models.CharField(max_length=15, null=False, default='null')
    transaction_type = models.CharField(max_length=15, null=False)
    transaction_amount = models.FloatField(null=False, validators=[MinValueValidator(0.0)])
    initiated_date = models.DateField(default=timezone.now())
    posted_date = models.DateField()
    status = models.CharField(max_length=15, null=False)

    def __str__(self):
        return str(self.id) + ' acct no.' + str(self.account.id) + ' ' + self.status

    class Meta:
        order_with_respect_to = 'account'



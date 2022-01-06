from django import forms
from django.utils import timezone

from .validators import validate_negative


class CustomerForm(forms.Form):
    PREFERRED = [
        (True, 'Yes'),
        (False, 'No')
    ]
    first_name = forms.CharField(max_length=25, label='First Name', required=True)
    last_name = forms.CharField(max_length=25, label='Last Name', required=True)
    ssn = forms.CharField(max_length=11, label='SSN', required=True)
    customer_since = forms.DateField(label='Customer Since', required=False, widget=forms.DateInput)
    preferred_customer = forms.ChoiceField(label='Preferred Customer ', required=True, choices=PREFERRED)


class AddressForm(forms.Form):
    STATE_CHOICES = [
        ('SC', 'South Carolina'),
        ('NC', 'North Carolina'),
        ('GA', 'Georgia'),
        ('VA', 'Virginia'),
        ('MD', 'Maryland'),
        ('PA', 'Pennsylvania'),
        ('NJ', 'New Jersey'),
        ('DE', 'Delaware'),
        ('NY', 'New York'),
        ('CT', 'Connecticut')
    ]

    street = forms.CharField(required=True, label='Enter Street name')
    city = forms.CharField(required=True, label='Enter City')
    state = forms.ChoiceField(required=True, label='State', choices=STATE_CHOICES)
    zip = forms.CharField(required=True, label='Zip')


class AccountForm(forms.Form):
    ACCOUNT_CHOICES = [
        ('CH', 'Checking'),
        ('SA', 'Savings'),
        ('IN', 'Investment')
    ]

    account_number = forms.CharField(max_length=20, label='Account Number', required=True)
    account_type = forms.ChoiceField(label='Account Type', required=True, widget=forms.RadioSelect,
                                     choices=ACCOUNT_CHOICES)
    balance = forms.FloatField(label='Account Balance', required=True, initial=1000, disabled=True)


class TransactionForm(forms.Form):
    TYPE = [
        ('1', 'Debit'),
        ('2', 'Credit')
    ]
    # status_c = [
    #     ('P', 'Pending'),
    #     ('C', 'Completed')
    # ]
    ACTIONS = [
        ('W', 'Withdraw'),
        ('D', 'Deposit')
    ]
    action = forms.ChoiceField(required=True, widget=forms.RadioSelect,
                               choices=ACTIONS)
    transaction_type = forms.ChoiceField(label='Transaction Type', required=True, choices=TYPE)
    transaction_amount = forms.FloatField(label='Transaction Amount', required=True, validators=[validate_negative])
    initiated_date = forms.DateField(label='Initiated post', required=False, widget=forms.DateInput,
                                     initial=timezone.now(), disabled=True)
    # posted_date = forms.DateField(label='Customer Since', required=False, widget=forms.DateInput)
    # status = forms.ChoiceField(label='Status', required=True, choices=status_c)

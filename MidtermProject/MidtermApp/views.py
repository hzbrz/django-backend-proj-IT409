from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response


# Create your views here.
from .forms import CustomerForm, AddressForm, AccountForm, TransactionForm
from .models import Customer, Address, Account, Transaction
from .Serializers import CustomerSerializer, AddressSerializer, AccountSerializer



def details(request):
    customers = Customer.objects.all()
    address = Address.objects.all()
    account = Account.objects.all()
    transaction = Transaction.objects.all()
    return render(request, 'home.html', {'customers': customers,
                                         'address': address,
                                         'account': account,
                                         'transaction': transaction
                                         })


class CreateCustomerView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'MidtermApp.add_customer'

    def get(self, request):
        form = CustomerForm
        return render(request, 'createCustomer.html', {'form': form})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            customer = Customer(first_name=cd['first_name'], last_name=cd['last_name'], ssn=cd['ssn'],
                                customer_since=cd['customer_since'], preferred_customer=cd['preferred_customer'])

            customer.save()
        else:
            print(form.errors)
            return render(request, 'createCustomer.html', {'form': form})
        return HttpResponseRedirect(reverse('home'))


class EditCustomerView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'MidtermApp.change_customer'

    def get(self, request, *args, **kwargs):
        print(" id = " + str(kwargs.get("id")))

        customer = Customer.objects.get(id=kwargs.get("id"))
        form = CustomerForm(initial={"first_name": customer.first_name, "last_name": customer.last_name,
                                     'ssn': customer.ssn, "customer_since": customer.customer_since,
                                     "preferred_customer": customer.preferred_customer})
        return render(request, 'createCustomer.html', {'form': form})

    def post(self, request, *args, **kwargs):
        print(" id = " + str(kwargs.get("id")))
        form = CustomerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            customer = Customer.objects.get(id=kwargs.get("id"))
            customer.first_name = cd['first_name']
            customer.last_name = cd['last_name']
            customer.ssn = cd['ssn']
            customer.customer_since = cd['customer_since']
            customer.preferred_customer = cd['preferred_customer']
            customer.save()
        else:
            print(form.errors)
            return render(request, 'createCustomer.html', {'form': form})
        return HttpResponseRedirect(reverse('home'))


@login_required()
@permission_required('MidtermApp.add_address', raise_exception=True)
def createAddress(request, fk):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(id=fk)
            cd = form.cleaned_data
            address = Address(street=cd['street'], city=cd['city'],
                              state=cd['state'], zip=cd['zip'])
            address.customer = customer
            address.save()
        else:
            print(form.errors)
            return render(request, 'createCustomer.html', {'form': form})
        return HttpResponseRedirect(reverse('home'))
    else:
        form = AddressForm
        return render(request, 'createCustomer.html', {'form': form})


@login_required()
@permission_required('MidtermApp.change_address', raise_exception=True)
def editAddress(request, id, fk):
    if request.method == 'POST':
        form = AddressForm(request.POST)                         # -5 points in Midterm here because I had AccountForm() instead of AddressForm()
        if form.is_valid():
            cd = form.cleaned_data
            address = Address.objects.get(id=id)
            customer = Customer.objects.get(id=fk)
            address.customer = customer
            address.street = cd['street']
            address.city = cd['city']
            address.state = cd['state']
            address.zip = cd['zip']
            address.save()
        else:
            print(form.errors)
            return render(request, 'createCustomer.html', {'form': form})
        return HttpResponseRedirect(reverse('home'))
    else:
        address = Address.objects.get(id=id)
        customer = Customer.objects.get(id=fk)
        address.customer = customer
        form = AddressForm(initial={'street': address.street, 'city': address.city,
                                    'state': address.state, 'zip': address.zip})

        return render(request, 'createCustomer.html', {'form': form})


@login_required()
@permission_required('MidtermApp.add_account', raise_exception=True)
def createAccount(request, fk):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(id=fk)
            cd = form.cleaned_data
            account = Account(account_number=cd['account_number'], account_type=cd['account_type'],
                              balance=cd['balance'])
            account.customer = customer
            account.save()
        else:
            print(form.errors)
            return render(request, 'createAccount.html', {'form': form})
        return HttpResponseRedirect(reverse('home'))
    else:
        form = AccountForm
        return render(request, 'createAccount.html', {'form': form})


@login_required()
@permission_required('MidtermApp.change_account', raise_exception=True)
def editAccount(request, id, fk):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            account = Account.objects.get(id=id)
            customer = Customer.objects.get(id=fk)
            account.customer = customer
            account.account_number = cd['account_number']
            account.account_type = cd['account_type']
            account.balance = cd['balance']
            account.save()
        else:
            print(form.errors)
            return render(request, 'createAccount.html', {'form': form})
        return HttpResponseRedirect(reverse('home'))
    else:
        account = Account.objects.get(id=id)
        customer = Customer.objects.get(id=fk)
        account.customer = customer
        form = AccountForm(initial={'account_number': account.account_number,
                                    'account_type': account.account_type, 'balance': account.balance})

        return render(request, 'createAccount.html', {'form': form})


class AddTransactionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        print(" fk = " + str(kwargs.get("fk")))
        form = TransactionForm
        return render(request, 'transaction.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            account = Account.objects.get(id=kwargs.get("fk"))
            cd = form.cleaned_data
            transaction = Transaction(action=cd['action'],
                                      transaction_type=cd['transaction_type'],
                                      transaction_amount=cd['transaction_amount'],
                                      initiated_date=cd['initiated_date'],
                                      posted_date=timezone.now() + timezone.timedelta(days=1),
                                      status='Pending')
            transaction.account = account
            if request.POST['action'] == 'W':
                if (account.balance - cd['transaction_amount']) < 0:
                    print('Withdraw error: balance is negative')
                    return render(request, 'transactionError.html', {'fk': kwargs.get('fk')})
                else:
                    print('Withdrawing... new balance is:', account.balance - cd['transaction_amount'])
                    balance = account.balance - cd['transaction_amount']
                    account.balance = balance
                    account.save()
                    transaction.save()
            else:
                print('Depositing... new balance is:', account.balance + cd['transaction_amount'])
                balance = account.balance + cd['transaction_amount']
                account.balance = balance
                account.save()
                transaction.save()
        else:
            print(form.errors)
            return render(request, 'transaction.html', {'form': form})
        return HttpResponseRedirect(reverse('home'))


# ListCreateAPIVIew – Customer, Address, Account
class CustomerListCreate(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.create(serializer.validated_data)
            return Response(CustomerSerializer(customer).data)

class AddressListCreate(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            address = serializer.create(serializer.validated_data)
            return Response(AddressSerializer(address).data)

class AccountListCreate(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.create(serializer.validated_data)
            return Response(AccountSerializer(account).data)

# RetrieveUpdateAPIView – Customer, Address, Account
class CustomerViewUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        customer = Customer.objects.get(id=pk)
        customerData = CustomerSerializer(customer)
        return Response(customerData.data)

    def update(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            print("Updating Customer = " + str(customer.id))
            updated_customer = serializer.update(customer, serializer.validated_data)
            print("Updated Customer = " + str(updated_customer.id))
            return Response(serializer.data)
        return Response(serializer.errors)

class AddressViewUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = AddressSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        address = Address.objects.get(id=pk)
        addressData = AddressSerializer(address)
        return Response(addressData.data)

    def update(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        address = Address.objects.get(id=pk)
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            print("Updating Address = " + str(address.id))
            address_customer = serializer.update(address, serializer.validated_data)
            print("Updated Address = " + str(address_customer.id))
            return Response(serializer.data)
        return Response(serializer.errors)

class AccountViewUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = AccountSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        account = Account.objects.get(id=pk)
        accountData = AccountSerializer(account)
        return Response(accountData.data)

    def update(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        account = Account.objects.get(id=pk)
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            print("Updating Account = " + str(account.id))
            account_customer = serializer.update(account, serializer.validated_data)
            print("Updated Account = " + str(account_customer.id))
            return Response(serializer.data)
        return Response(serializer.errors)




from rest_framework import serializers
from .models import Customer, Address, Account, Transaction

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.ssn = validated_data.get('snn', instance.ssn)
        instance.customer_since = validated_data.get('customer_since', instance.customer_since)
        instance.preferred_customer = validated_data.get('preferred_customer', instance.preferred_customer)

        instance.save()
        return instance

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.customer = validated_data.get('customer', instance.customer)
        instance.street = validated_data.get('street', instance.street)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.zip = validated_data.get('zip', instance.zip)

        instance.save()
        return instance

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.customer = validated_data.get('customer', instance.customer)
        instance.account_number = validated_data.get('account_number', instance.account_number)
        instance.account_type = validated_data.get('account_type', instance.account_type)
        instance.balance = validated_data.get('balance', instance.balance)

        instance.save()
        return instance

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.account = validated_data.get('account', instance.account)
        instance.transaction_type = validated_data.get('transaction_type', instance.transaction_type)
        instance.transaction_amount = validated_data.get('transaction_amount', instance.transaction_amount)
        instance.initiated_date = validated_data.get('initiated_date', instance.initiated_date)
        instance.posted_date = validated_data.get('posted_date', instance.posted_date)
        instance.status = validated_data.get('status', instance.status)

        instance.save()
        return instance


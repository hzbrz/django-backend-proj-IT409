from rest_framework import viewsets
from rest_framework.response import Response

from .Serializers import TransactionSerializer
from .models import Transaction, Account


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def retrieve(self, request, *args, **kwargs):
        transaction = Transaction.objects.get(id=kwargs['pk'])
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        account = request.data['account']
        print(f'{request.data} \nAccount: {request.data["account"]}\n')
        print(f'Account data: {account}')

        if serializer.is_valid():
            transaction = serializer.save()
            """"
            While testing the transaction viewset and creating a new transaction,
            you will see a new field named 'Action' which determines how the transaction will be handled.
            Fill the Action field with W (uppercase) for withdraw or D (uppercase) or deposit.  
            """
            if transaction.action == 'W':
                if (transaction.account.balance - transaction.transaction_amount) < 0:
                    print('Withdraw error: balance is negative')
                else:
                    print('Withdrawing... new balance is:', transaction.account.balance - transaction.transaction_amount)
                    balance = transaction.account.balance - transaction.transaction_amount
                    transaction.account.balance = balance
                    transaction.account.save()
            else:
                print('Depositing... new balance is:', transaction.account.balance - transaction.transaction_amount)
                balance = transaction.account.balance + transaction.transaction_amount
                transaction.account.balance = balance
                transaction.account.save()

            return Response(TransactionSerializer(transaction).data)
        else:
            print(serializer.error_messages)
            return Response({"message": "Could not create the Transaction"})

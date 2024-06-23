from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status
from expense.api.serializers import UserSerializer, ExpenseSerializer, ExpenseItemSerializer
from expense.models import User, Expense, ExpenseItem


class CreateUser(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()


class ExpenseItemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ExpenseItemSerializer
    queryset = Expense.objects.all()

class MyExpenseAPIView(APIView):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        expense_items = ExpenseItem.objects.filter(participants=user)
        debt_items = expense_items.exclude(expense__payer=user)
        you_owe_to = {}
        total_debt = 0
        for item in debt_items:
            participants_count = item.participants.count()
            temp_debt = item.final_amount // participants_count
            due_to = item.expense.payer.email
            if due_to in you_owe_to:
                you_owe_to[due_to] += temp_debt
            else:
                you_owe_to[due_to] = temp_debt
            total_debt += temp_debt
        
        given_to = expense_items.filter(expense__payer=user)
        amount_given = 0
        who_owed_you = {}
        for item in given_to:
            participants_count = item.participants.count()
            for owed_user in item.participants.all():
                if owed_user == user:
                    continue
                amount_given += item.final_amount // participants_count
                if owed_user.email in who_owed_you:
                    who_owed_you[owed_user.email] += item.final_amount // participants_count
                else:
                    who_owed_you[owed_user.email] = item.final_amount // participants_count
        
        return Response({
            "Total Balance": amount_given - total_debt,
            "Total You are Owed": amount_given or 0,
            "Total You Owe": total_debt or 0,
            "You Owe To": you_owe_to or "No One",
            "Owed To You": who_owed_you or "No One",
        }, status=status.HTTP_200_OK)



class FriendExpenseAPIView(APIView):
    def get(self, request, pk):
        friend_id = request.GET.get('friend')
        user = User.objects.get(id=pk)
        friend = User.objects.get(id=friend_id)
        expenses = Expense.objects.filter(items__participants=friend).distinct()
        expense_list = []
        for expense in expenses:
            temp_expense = {
                'id': expense.id,
                'date': expense.date.date(),
                'description': expense.description,
                'Paid By': expense.payer.email
            }
            if expense.payer != user:
                temp_expense['Total You Borrowed'] = expense.get_borrowed_amount(user)
            else:
                temp_expense['Total Owed To You'] = expense.amount_owed_by_friend(friend)
            expense_list.append(temp_expense)
        return Response({'Expenses': expense_list}, status=status.HTTP_200_OK)

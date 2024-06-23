from rest_framework import serializers
from expense.models import Expense, ExpenseItem
from expense.models import User
from django.db.models import Sum

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class ExpenseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseItem
        fields = '__all__'
        extra_kwargs = {'expense': {'required': False}}
        read_only_fields = ['final_amount']


class ExpenseSerializer(serializers.ModelSerializer):
    items = ExpenseItemSerializer(many=True)

    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        expense = super().create(validated_data)
        try:
            for item_data in items_data:
                participants = item_data.pop('participants')
                item_data['expense'] = expense.id
                item_serializer = ExpenseItemSerializer(data=item_data)
                item_serializer.is_valid(raise_exception=True)
                new_item = item_serializer.save()
                for user in participants:
                    new_item.participants.add(user)
                new_item.save()
            total_amount = expense.items.all().aggregate(total_amount=Sum('final_amount'))['total_amount']
            expense.total_amount = total_amount + expense.tip
            expense.save()
        except Exception as e:
            expense.delete()
            raise serializers.ValidationError(str(e))
        return expense

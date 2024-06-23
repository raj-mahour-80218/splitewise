from django.contrib import admin
from .models import User, Expense, ExpenseItem
# Register your models here.

admin.site.register(User)
admin.site.register(Expense)
admin.site.register(ExpenseItem)
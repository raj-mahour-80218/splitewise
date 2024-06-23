from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from expense.managers import CustomUserManager



class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Expense(models.Model):
    description = models.CharField(max_length=120, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    total_amount = models.FloatField(blank=True, null=True)
    tip = models.FloatField(default=0)
    payer = models.ForeignKey(User, related_name="expenses_paid", on_delete=models.CASCADE)

    def get_borrowed_amount(self, user):
        total_debt = 0
        items = self.items.filter(participants=user)
        for item in items:
            participants_count = item.participants.count()
            temp_debt = item.final_amount // participants_count
            total_debt += temp_debt
        return total_debt
    
    def amount_owed_by_friend(self, friend):
        items = self.items.filter(participants=friend)
        amount_given = 0
        for item in items:
            participants_count = item.participants.count()
            amount_given += item.final_amount // participants_count
        return amount_given


class ExpenseItem(models.Model):
    expense = models.ForeignKey(Expense, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=120, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    participants = models.ManyToManyField(User, blank=True, related_name="expense_items")
    tax = models.FloatField(blank=True, null=True)
    final_amount = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        amount = self.price + (self.price * self.tax / 100)
        self.final_amount = amount
        return super().save(*args, **kwargs)

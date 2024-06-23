from django.urls import path, include
from rest_framework.routers import DefaultRouter
from expense.api.api_views import (
    ExpenseViewSet,
    MyExpenseAPIView,
    FriendExpenseAPIView,
    CreateUser,
    ExpenseItemViewSet
)


router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet)
router.register(r'expenseitem', ExpenseItemViewSet, basename="expense-item")


urlpatterns = [
    path('', include(router.urls)),
    path('create-user/', CreateUser.as_view(), name='create-user'),
    path('my-expenses/<int:pk>/', MyExpenseAPIView.as_view(),
         name='my-expenses'),
    path('friend-expenses/<int:pk>/', FriendExpenseAPIView.as_view(),
         name='friend-expenses'),
]
from django.urls import path
from .views import TransactionBookViews

urlpatterns = [
    path('', TransactionBookViews.as_view()),
]
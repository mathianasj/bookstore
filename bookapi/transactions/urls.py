from django.urls import path
from .views import TransactionViews, TransactionListView

urlpatterns = [
    path('', TransactionListView.as_view()),
    path('<int:id>', TransactionViews.as_view())
]
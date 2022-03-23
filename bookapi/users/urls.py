from django.urls import path
from .views import UserViews

urlpatterns = [
    path('/', UserViews.as_view()),
    path('/<int:id>', UserViews.as_view())
]
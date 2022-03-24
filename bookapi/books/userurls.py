from django.urls import path
from .views import UserBookViews

urlpatterns = [
    path('', UserBookViews.as_view()),
]
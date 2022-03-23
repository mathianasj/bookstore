from django.urls import path
from .views import BookViews

urlpatterns = [
    path('', BookViews.as_view()),
    path('<int:id>', BookViews.as_view())
]
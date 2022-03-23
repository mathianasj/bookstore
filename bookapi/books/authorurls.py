from django.urls import path
from .views import AuthorViews

urlpatterns = [
    path('', AuthorViews.as_view()),
    path('<int:id>', AuthorViews.as_view())
]
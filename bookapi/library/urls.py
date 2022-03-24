from django.urls import path
from .views import LibraryViews

urlpatterns = [
    path('', LibraryViews.as_view()),
    path('<int:id>', LibraryViews.as_view())
]
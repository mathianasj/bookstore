from django.urls import path
from .views import LibraryBookViews, LibraryViews

urlpatterns = [
    path('', LibraryViews.as_view()),
    path('<int:id>', LibraryViews.as_view()),
    path('<int:id>/books', LibraryBookViews.as_view())
]
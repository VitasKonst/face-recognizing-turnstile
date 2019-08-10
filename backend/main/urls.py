from django.urls import path
from .views import PassViewModel


urlpatterns = [
    path('', PassViewModel.as_view()),
]

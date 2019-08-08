from django.urls import re_path, path
from .views import LoginAPIView, UserRetrieveUpdateAPIView

urlpatterns = [
    re_path('login/?$', LoginAPIView.as_view()),
    path('user/<int:pk>', UserRetrieveUpdateAPIView.as_view()),
]

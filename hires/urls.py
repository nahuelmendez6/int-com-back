from django.urls import path
from .views import HireAPIView

urlpatterns = [
    path('', HireAPIView.as_view(), name='hires-list'),
]

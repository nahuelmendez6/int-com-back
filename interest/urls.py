from django.urls import path

from .views import InterestAPIView

urlpatterns = [

    path('', InterestAPIView.as_view(), name='interest-list-create'),
    path('<int:pk>/', InterestAPIView.as_view(), name='interest-detail'),

]
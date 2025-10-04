from django.urls import path

from .views import PetitionAPIView

urlpatterns = [

    path('', PetitionAPIView.as_view(), name='petition-create')

]
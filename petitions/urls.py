from django.urls import path

from .views import PetitionAPIView, TypePetitionAPIView

urlpatterns = [

    # URL para creacion o para consumo de multiples peticiones
    path('', PetitionAPIView.as_view(), name='petition-create'),

    # URL para consumo/edicion de peticiones individuales
    path('<int:pk>/', PetitionAPIView.as_view(), name='petition-detail'),

    # URL para consumo de TypePetition
    path('type-petitions/', TypePetitionAPIView.as_view(), name='type-petition'),
]


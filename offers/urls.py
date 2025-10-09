from django.urls import path
from .views import (
    TypeOfferListCreateAPIView, TypeOfferDetailAPIView,
    OfferListCreateAPIView, OfferDetailAPIView, CustomerOfferFeedAPIView
)

urlpatterns = [
    # TypeOffer
    path('type-offers/', TypeOfferListCreateAPIView.as_view(), name='typeoffer-list-create'),
    path('type-offers/<int:pk>/', TypeOfferDetailAPIView.as_view(), name='typeoffer-detail'),

    # Offer
    path('', OfferListCreateAPIView.as_view(), name='offer-list-create'),
    path('<int:pk>/', OfferDetailAPIView.as_view(), name='offer-detail'),

    # Filtro de ofertas para cliente
    path('customer-feed/', CustomerOfferFeedAPIView.as_view(), name='customer-offers-feed'),
]

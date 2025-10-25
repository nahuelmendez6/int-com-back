from django.urls import path
from .views import (GradeProviderAPIView, 
                    GradeProviderDetailAPIView, 
                    ProviderAverageRatingView,
                    GradeCustomerAPIView,
                    GradeCustomerDetailAPIView)

urlpatterns = [
    # Listar todas las calificaciones / Crear nueva calificación
    path('', GradeProviderAPIView.as_view(), name='gradeprovider-list-create'),

    # Detalle y actualización de una calificación específica
    path('<int:id>/', GradeProviderDetailAPIView.as_view(), name='gradeprovider-detail'),

    path('average-rating/<int:provider_id>/', ProviderAverageRatingView.as_view(), name='provider-average-rating'),


    path('grades-customer/', GradeCustomerAPIView.as_view(), name='grades-customer'),
    path('grades-customer/<int:id>/', GradeCustomerDetailAPIView.as_view(), name='grade-customer-detail'),
]

from django.urls import path
from .views import (
    PortfolioAPIView,
    PortfolioDetailAPIView,
    PortfolioAttachmentAPIView,
    PortfolioAttachmentDetailAPIView
)

urlpatterns = [
    path('portfolios/', PortfolioAPIView.as_view(), name='portfolio-list-create'),
    path('portfolios/<int:id_portfolio>/', PortfolioDetailAPIView.as_view(), name='portfolio-detail'),
    path('portfolio-attachments/', PortfolioAttachmentAPIView.as_view(), name='attachment-list-create'),
    path('portfolio-attachments/<int:id_attachment>/', PortfolioAttachmentDetailAPIView.as_view(), name='attachment-detail'),
]

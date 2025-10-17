from django.urls import path
from .views import (
    PortfolioAPIView,
    PortfolioDetailAPIView,
    PortfolioAttachmentAPIView,
    PortfolioAttachmentDetailAPIView
)

urlpatterns = [
    path('', PortfolioAPIView.as_view(), name='portfolio-list-create'),
    path('<int:id_portfolio>/', PortfolioDetailAPIView.as_view(), name='portfolio-detail'),
    path('attachments/', PortfolioAttachmentAPIView.as_view(), name='attachment-list-create'),
    path('attachments/<int:id_attachment>/', PortfolioAttachmentDetailAPIView.as_view(), name='attachment-detail'),
]

from django.urls import path
from .views import (
    PortfolioAPIView,
    PortfolioDetailAPIView,
    PortfolioAttachmentAPIView,
    PortfolioAttachmentDetailAPIView,
    MaterialAPIView,
    MaterialDetailAPIView,
    MaterialAttachmentDetailAPIView,
    MaterialAttachmentAPIView
)

urlpatterns = [
    path('', PortfolioAPIView.as_view(), name='portfolio-list-create'),
    path('<int:id_portfolio>/', PortfolioDetailAPIView.as_view(), name='portfolio-detail'),
    path('attachments/', PortfolioAttachmentAPIView.as_view(), name='attachment-list-create'),
    path('attachments/<int:id_attachment>/', PortfolioAttachmentDetailAPIView.as_view(), name='attachment-detail'),
    
    path('materials/<int:id_material>/', MaterialDetailAPIView.as_view(), name='material-detail'),
    path('materials/', MaterialAPIView.as_view(), name='material'),
    path('materials/<int:id_provider>', MaterialAPIView.as_view(), name='material-provider'),
    path('material-attachment/', MaterialAttachmentAPIView.as_view(), name='material-attachment'),
    path('material-attachment/<int:id_material_attachment>/', MaterialAttachmentDetailAPIView.as_view(), name='material-attachment')

]

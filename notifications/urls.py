from django.urls import path
from . import views

urlpatterns = [
    # CRUD de notificaciones
    path('', views.NotificationListCreateView.as_view(), name='notification-list-create'),
    path('<int:pk>/', views.NotificationRetrieveUpdateDestroyView.as_view(), name='notification-detail'),
    
    # Acciones específicas
    path('mark-all-read/', views.mark_all_as_read, name='mark-all-read'),
    path('<int:notification_id>/mark-read/', views.mark_notification_as_read, name='mark-notification-read'),
    
    # Estadísticas y datos
    path('stats/', views.notification_stats, name='notification-stats'),
    path('unread-count/', views.get_unread_count, name='unread-count'),
    path('recent/', views.get_recent_notifications, name='recent-notifications'),
    path('types/', views.get_notification_types, name='notification-types'),
    
    # Configuración
    path('settings/', views.NotificationSettingsView.as_view(), name='notification-settings'),
]

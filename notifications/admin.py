from django.contrib import admin
from .models import Notification, NotificationSettings

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'read_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('user', 'title', 'message', 'notification_type')
        }),
        ('Estado', {
            'fields': ('is_read', 'read_at')
        }),
        ('Relaciones', {
            'fields': ('related_postulation_id', 'related_petition_id')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'push_notifications', 'created_at']
    list_filter = ['email_notifications', 'push_notifications', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Configuración por Tipo', {
            'fields': (
                'postulation_created', 'postulation_state_changed',
                'postulation_accepted', 'postulation_rejected',
                'petition_closed'
            )
        }),
        ('Configuración General', {
            'fields': ('email_notifications', 'push_notifications')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

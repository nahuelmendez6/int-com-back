from django.contrib import admin
from .models import Portfolio, PortfolioAttachment

# Register your models here.
@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('id_portfolio', 'name', 'description')

@admin.register(PortfolioAttachment)
class PortfolioAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id_attachment', 'file', 'file_type')
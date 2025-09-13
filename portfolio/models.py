from django.db import models

class Portfolio(models.Model):

    """
    Modelo encargado de gestionar la tabla n_portfolio
    """

    id_portfolio = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    id_provider = models.ForeignKey(
        'authentication.Provider',
        on_delete=models.CASCADE,
        db_column='id_provider',
        related_name='provider_portfolio',
        primary_key=True
    ),
    id_user_create = models.IntegerField(null=True, blank=True),
    id_user_update = models.IntegerField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'n_portfolio'
        managed = False

    def __str__(self):
        return self.title
    

class PortfolioAttachment(models.Model):

    class FileType(models.TextChoices):
        IMAGE = 'image', 'Imagen'
        VIDEO = 'video', 'Video'
        DOCUMENT = 'document', 'Documento'
        OTHER = 'other', 'Otro'

    """
    Modelo encargado de gestionar la tabla n_portfolio_attachment
    """

    id_attachment = models.AutoField(primary_key=True),
    id_portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        db_column='id_portfolio',
        related_name='portfolio_attachments'
    ),
    file_name = models.CharField(max_length=255),
    file_path = models.CharField(max_length=500),
    file_type = models.CharField(
        max_length=10,
        choices=FileType.choices,
        default=FileType.OTHER)
    mime_type = models.CharField(max_length=100, null=True, blank=True)
    file_sizwe = models.IntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    id_user_upload = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'n_portfolio_attachment'
        managed = False

    def __str__(self):
        return f"Attachment {self.id_portfolio_attachment} for Portfolio {self.id_portfolio_id}"
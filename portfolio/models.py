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
    )
    id_user_create = models.IntegerField(null=True, blank=True)
    id_user_update = models.IntegerField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

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

    id_attachment = models.AutoField(primary_key=True)
    id_portfolio = models.ForeignKey(
        'Portfolio',
        on_delete=models.CASCADE,
        db_column='id_portfolio',
        related_name='attachments'
    )
    file = models.FileField(upload_to='portfolio_attachments/')
    file_type = models.CharField(
        max_length=10,
        choices=FileType.choices,
        default=FileType.OTHER
    )
    mime_type = models.CharField(max_length=100, null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    id_user_upload = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'n_portfolio_attachment'
        managed = False  # True si querés que Django maneje la tabla

    def __str__(self):
        return f"{self.file.name} ({self.file_type})"


class Material(models.Model):
    id_material = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    id_provider = models.IntegerField()  # FK a n_provider
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    unit = models.CharField(max_length=20, default='unidad')
    description = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'n_material'
        managed = False

    def __str__(self):
        return self.name
    

class MaterialAttachment(models.Model):

    id_material_attachment = models.AutoField(primary_key=True)
    id_material = models.ForeignKey(
        'Material',
        on_delete=models.CASCADE,
        db_column='id_material',
        related_name='material_attachments'
    )
    file = models.FileField(upload_to='material_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    id_user_upload = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'n_material_attachment'
        managed = False  # True si querés que Django maneje la tabla

    def __str__(self):
        return f"{self.file.name} ({self.file_type})"
from django.db import models


# ====================================================
# Modelo: Portfolio
# ====================================================
class Portfolio(models.Model):

    """
    Modelo que representa el portafolio de un proveedor.
    Gestiona la tabla 'n_portfolio' y permite asociar información
    y archivos (PortfolioAttachment) relacionados a un proveedor.
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
    

# ====================================================
# Modelo: PortfolioAttachment
# ====================================================
class PortfolioAttachment(models.Model):
    """
    Archivos asociados a un portafolio.
    Permite almacenar imágenes, videos, documentos u otros tipos de archivos.
    """
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

# ====================================================
# Modelo: Material
# ====================================================
class Material(models.Model):
    """
    Materiales que un proveedor ofrece.
    Gestiona la tabla 'n_material' y permite asociar archivos (MaterialAttachment)
    """
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
    
# ====================================================
# Modelo: MaterialAttachment
# ====================================================
class MaterialAttachment(models.Model):
    """
    Archivos asociados a un material.
    Permite almacenar imágenes, documentos u otros archivos relacionados al material.
    """

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
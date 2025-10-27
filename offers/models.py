from django.db import models


# ====================================================
# Modelo: TypeOffer
# ====================================================
class TypeOffer(models.Model):
    """
    Modelo que representa los tipos de ofertas.
    Campos:
    - id_type_offer: PK auto incremental
    - name: nombre del tipo de oferta
    - id_user_create / id_user_update: usuarios que crearon/actualizaron el registro
    - date_create / date_update: timestamps de creación y actualización
    """
    id_type_offer = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    id_user_create = models.IntegerField(null=True, blank=True)
    id_user_update = models.IntegerField(null=True, blank=True)

    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'n_type_offer'
        managed = False

    def __str__(self):
        return self.name

# ====================================================
# Manager personalizado: OfferManager
# ====================================================
class OfferManager(models.Manager):
    """
    Manager personalizado para el modelo Offer.
    Filtra automáticamente los registros marcados como eliminados (soft delete).
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


# ====================================================
# Modelo: Offer
# ====================================================
class Offer(models.Model):
    """
    Modelo que representa una oferta publicada por un proveedor.
    Campos principales:
    - offer_id: PK auto incremental
    - id_type_offer: FK al tipo de oferta (TypeOffer)
    - name, description: información de la oferta
    - date_open, date_close: rango de validez de la oferta
    - status: estado de la oferta (draft, active, closed, archived)
    - id_provider: proveedor que creó la oferta
    - user_create_id / user_update_id: usuarios que crearon/actualizaron
    - date_create / date_update: timestamps de creación y actualización
    - is_deleted: soft delete
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]

    offer_id = models.AutoField(primary_key=True)

    id_type_offer = models.ForeignKey(
        TypeOffer,
        on_delete=models.PROTECT,
        db_column='id_type_offer'
    )

    name = models.CharField(max_length=150)
    description = models.TextField()

    date_open = models.DateTimeField()
    date_close = models.DateTimeField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft"
    )

    id_provider = models.IntegerField()  # FK a n_provider (puedes hacer modelo si quieres)

    user_create_id = models.IntegerField(null=True, blank=True)
    user_update_id = models.IntegerField(null=True, blank=True)

    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    # Soft delete
    is_deleted = models.BooleanField(default=False)

    # Managers
    objects = OfferManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'n_offers'
        managed = False

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        """Soft delete: no borra, solo marca como eliminado"""
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

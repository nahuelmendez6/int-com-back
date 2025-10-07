from django.db import models


class TypeOffer(models.Model):
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


class OfferManager(models.Manager):
    """
    Manager personalizado para soft delete: excluye los registros marcados como eliminados
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Offer(models.Model):
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

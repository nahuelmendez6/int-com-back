from django.db import models

# ====================================================
# Modelo Interest
# ====================================================
class Interest(models.Model):

    """
    Representa los intereses de un cliente en determinadas categorías.

    Campos:
    - id_interest: PK automática de la tabla.
    - id_customer: FK al cliente que tiene el interés.
    - id_category: FK a la categoría de interés.
    - id_user_create / id_user_update: IDs de usuarios que crearon/actualizaron el registro.
    - date_create / date_update: Timestamps de creación y actualización.
    - is_deleted: Para soft delete, indica si el registro está eliminado lógicamente.
    """
    id_interest = models.AutoField(primary_key=True)
    id_customer = models.ForeignKey(
        'authentication.Customer',
        on_delete=models.PROTECT,
        db_column='id_customer'
    )
    id_category = models.ForeignKey(
        'profiles.Category',
        on_delete=models.PROTECT,
        db_column='id_category'
    )
    id_user_create = models.IntegerField(null=True, blank=True)
    id_user_update = models.IntegerField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    # Campo para soft delete
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'n_interest'
        managed = False


    # ====================================================
    # Método de borrado lógico (soft delete)
    # ====================================================
    def delete(self, using=None, keep_parents=False):
        """Soft delete: no borra, solo marca como eliminado"""
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

from django.db import models


def petition_upload_path(instance, filename):
    """
    Función para definir la ruta de subida de archivos adjuntos a la petición.
    La ruta será: petitions/<id_petition>/<filename>
    """
    return f"petitions/{instance.id_petition.id_petition}/{filename}"

# ====================================================
# MODELO: TypePetition
# ====================================================
class TypePetition(models.Model):
    """
    Modelo que define los tipos de peticiones que pueden existir en la plataforma.
    Ejemplo: Solicitud de materiales, servicios, proyectos, etc.
    """
    
    id_type_petition = models.AutoField(primary_key=True)
    type_petition = models.CharField(max_length=100)
    id_user_create = models.IntegerField(null=True, blank=True)
    id_user_update = models.IntegerField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'n_type_petition'
        managed = False

# ====================================================
# MODELO: PetitionState
# ====================================================
class PetitionState(models.Model):
    """
    Modelo que define los posibles estados de una petición.
    Ejemplo: Abierta, Cerrada, En proceso, Finalizada.
    """

    id_state = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'n_petition_state'
        managed = False

# ====================================================
# MANAGER PERSONALIZADO: PetitionManager
# ====================================================
class PetitionManager(models.Manager):
    """
    Manager personalizado para implementar soft delete.
    Solo devuelve los registros no eliminados (is_deleted=False)
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

# ====================================================
# MODELO: Petition
# ====================================================
class Petition(models.Model):
    """
    Modelo principal de Peticiones.
    Contiene información general de la petición, tipo, cliente, fechas, estado,
    categoría y relaciones con profesiones y tipos de proveedores.
    Implementa soft delete mediante el campo 'is_deleted' y manager personalizado.
    """
    id_petition = models.AutoField(primary_key=True)
    id_type_petition = models.ForeignKey(TypePetition, on_delete=models.PROTECT, db_column='id_type_petition')
    id_customer = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    id_profession = models.ForeignKey('profiles.Profession', on_delete=models.SET_NULL, db_column='id_profession', null=True, blank=True)
    id_type_provider = models.ForeignKey('profiles.TypeProvider', on_delete=models.SET_NULL, db_column='id_type_provider', null=True, blank=True)
    id_state = models.ForeignKey(PetitionState, on_delete=models.SET_NULL, db_column='id_state', null=True, blank=True)
    date_since = models.DateField(null=True, blank=True)
    date_until = models.DateField(null=True, blank=True)
    id_user_create = models.IntegerField(null=True, blank=True)
    id_user_update = models.IntegerField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    categories = models.ManyToManyField('profiles.Category', through='PetitionCategory')

    # Campo para soft delete
    is_deleted = models.BooleanField(default=False)

    # Asignar manager personalizado
    objects = PetitionManager()
    all_objects = models.Manager()  # Incluye los borrados


    class Meta:
        db_table = 'n_petition'
        managed = False

    def delete(self, using=None, keep_parents=False):
        """Soft delete: no borra, solo marca como eliminado"""
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])


# ====================================================
# MODELO: PetitionCategory
# ====================================================
class PetitionCategory(models.Model):
    """
    Modelo intermedio para la relación ManyToMany entre Petition y Category.
    """
    id_petition_category = models.AutoField(primary_key=True)
    id_petition = models.ForeignKey(Petition, on_delete=models.CASCADE, db_column='id_petition')
    id_category = models.ForeignKey('profiles.Category', on_delete=models.CASCADE, db_column='id_category')

    class Meta:
        db_table = 'n_petition_category'
        managed = False

# ====================================================
# MODELO: PetitionAttachment
# ====================================================
class PetitionAttachment(models.Model):
    """
    Modelo para almacenar archivos adjuntos a una petición.
    Cada archivo se sube a la ruta definida por petition_upload_path.
    """
    id_petition_attachment = models.AutoField(primary_key=True)
    id_petition = models.ForeignKey(Petition, on_delete=models.CASCADE, db_column='id_petition')
    file = models.FileField(upload_to=petition_upload_path, db_column='url')
    # type = models.CharField(max_length=50)
    id_user_create = models.IntegerField(null=True, blank=True)
    id_user_update = models.IntegerField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'n_petition_attachment'
        managed = False

# ====================================================
# MODELO: PetitionMaterial
# ====================================================
class PetitionMaterial(models.Model):
    """
    Modelo para gestionar los materiales asociados a una petición.
    Contiene cantidad, precio unitario y referencias de creación/actualización.
    """
    id_petition_material = models.AutoField(primary_key=True)
    id_petition = models.ForeignKey(Petition, on_delete=models.CASCADE, db_column='id_petition')
    id_article = models.IntegerField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    id_user_create = models.IntegerField(null=True, blank=True)
    id_user_update = models.IntegerField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'n_petition_material'
        managed = False


# ====================================================
# MODELO: PetitionStateHistory
# ====================================================
class PetitionStateHistory(models.Model):
    """
    Modelo para almacenar el historial de cambios de estado de una petición.
    Permite auditar quién cambió el estado y cuándo.
    """
    id_petition_state_history = models.AutoField(primary_key=True)
    id_petition = models.ForeignKey(Petition, on_delete=models.CASCADE, db_column='id_petition')
    id_state = models.ForeignKey(PetitionState, on_delete=models.PROTECT, db_column='id_state')
    changed_by_user_id = models.IntegerField()
    note = models.CharField(max_length=255, null=True, blank=True)
    change_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'n_petition_state_history'
        managed = False
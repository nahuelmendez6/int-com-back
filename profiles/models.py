from django.db import models

# ====================================
# MODELO DE CATEGORÍAS
# ====================================
class Category(models.Model):
    """
    Representa las diferentes categorías que pueden asociarse a un proveedor.
    """
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'n_category'
        managed = False

    def __str__(self):
        return self.name
    

# ====================================
# MODELO DE TIPOS DE PROVEEDORES
# ====================================
class TypeProvider(models.Model):
    """
    Representa los diferentes tipos de proveedores disponibles en el sistema.
    Por ejemplo: "Empresa", "Freelance", "Autónomo", etc.
    """
    id_type_provider = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'n_type_provider'
        managed = False

    def __str__(self):
        return self.name
    
# ====================================
# MODELO DE PROFESIONES
# ====================================
class Profession(models.Model):
    """
    Representa las diferentes profesiones que pueden asociarse a un proveedor.
    """
    id_profession = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'n_profession'
        managed = False

    def __str__(self):
        return self.name



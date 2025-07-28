from django.db import models

class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'n_category'
        managed = False

class TypeProvider(models.Model):
    id_type_provider = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'n_type_provider'
        managed = False

class Profession(models.Model):
    id_profession = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'n_profession'
        managed = False



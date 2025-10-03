from django.db import models

# Create your models here.
class TypePetitions(models.Model):
    
    id_type_petition = models.AutoField(primary_key=True)
    type_petition = models.CharField(max_length=100)
    id_user_create = models.IntegerField(null=True, blank=True)
    id_user_update = models.IntegerField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'n_type_petition'
        managed = False


class PetitionState(models.Model):

    id_state = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'n_petition_state'
        managed = False
        
from django.db import models

# Create your models here.
class TypePetition(models.Model):
    
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


class Petition(models.Model):

    id_petition = models.AutoField(primary_key=True)
    id_type_petition = models.ForeignKey(TypePetition, on_delete=models.PROTECT, db_column='id_type_petition')
    id_customer = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    id_profession = models.ForeignKey('Profession', on_delete=models.SET_NULL, db_column='id_profession', null=True, blank=True)
    id_type_provider = models.ForeignKey('TypeProvider', on_delete=models.SET_NULL, db_column='id_type_provider', null=True, blank=True)
    id_state = models.ForeignKey(PetitionState, on_delete=models.SET_NULL, db_column='id_state', null=True, blank=True)
    date_since = models.DateField(null=True, blank=True)
    date_until = models.DateField(null=True, blank=True)
    id_user_create = models.IntegerField(null=True, blank=True)
    id_user_update = models.IntegerField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    categories = models.ManyToManyField('Category', through='PetitionCategory')

    class Meta:
        db_table = 'n_petition'
        managed = False


class PetitionCategory(models.Model):

    id_petition_category = models.AutoField(primary_key=True)
    id_petition = models.ForeignKey(Petition, on_delete=models.CASCADE, db_column='id_petition')
    id_category = models.ForeignKey('Category', on_delete=models.CASCADE, db_column='id_category')

    class Meta:
        db_table = 'n_petition_category'
        managed = False

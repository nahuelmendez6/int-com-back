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

    class Meta:
        db_table = 'n_petition'
        managed = False


class PetitionCategory(models.Model):

    id_petition_category = models.AutoField(primary_key=True)
    id_petition = models.ForeignKey(Petition, on_delete=models.CASCADE, db_column='id_petition')
    id_category = models.ForeignKey('profiles.Category', on_delete=models.CASCADE, db_column='id_category')

    class Meta:
        db_table = 'n_petition_category'
        managed = False


class PetitionAttachment(models.Model):

    id_petition_attachment = models.AutoField(primary_key=True)
    id_petition = models.ForeignKey(Petition, on_delete=models.CASCADE, db_column='id_petition')
    url = models.CharField(max_length=500)
    type = models.CharField(max_length=50)
    id_user_create = models.IntegerField(null=True, blank=True)
    id_user_update = models.IntegerField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'n_petition_attachment'
        managed = False


class PetitionMaterial(models.Model):
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


class PetitionStateHistory(models.Model):
    id_petition_state_history = models.AutoField(primary_key=True)
    id_petition = models.ForeignKey(Petition, on_delete=models.CASCADE, db_column='id_petition')
    id_state = models.ForeignKey(PetitionState, on_delete=models.PROTECT, db_column='id_state')
    changed_by_user_id = models.IntegerField()
    note = models.CharField(max_length=255, null=True, blank=True)
    change_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'n_petition_state_history'
        managed = False
from django.db import models

class Address(models.Model):
    id_address = models.AutoField(primary_key=True)
    # ...
    class Meta:
        db_table = 'n_address'
        managed = False
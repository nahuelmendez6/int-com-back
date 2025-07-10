from django.db import models

class Country(models.Model):
    id_country = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'country'
        managed = False

    def __str__(self):
        return self.name


class Province(models.Model):
    id_province = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_country',
        related_name='provinces'
    )
    date_create = models.DateTimeField(null=True, blank=True)
    date_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'n_province'
        managed = False

    def __str__(self):
        return self.name


class Department(models.Model):
    id_department = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_province',
        related_name='departments'
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_country',
        related_name='departments'
    )
    date_create = models.DateTimeField(null=True, blank=True)
    date_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'n_department'
        managed = False

    def __str__(self):
        return self.name


class City(models.Model):
    id_city = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_department',
        related_name='cities'
    )
    date_create = models.DateTimeField(null=True, blank=True)
    date_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'n_city'
        managed = False

    def __str__(self):
        return f"{self.name} ({self.postal_code})"


class Address(models.Model):
    id_address = models.AutoField(primary_key=True)
    # ...
    class Meta:
        db_table = 'n_address'
        managed = False


class Zone(models.Model):
    id_zone = models.AutoField(primary_key=True)

    class Meta:
        managed = False


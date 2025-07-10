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

    # para acceder a los proveedores asignados a una ciudad
    providers = models.ManyToManyField(
        'Provider',
        through='ProviderCity',
        related_name='served_cities'
    )

    class Meta:
        db_table = 'n_city'
        managed = False

    def __str__(self):
        return f"{self.name} ({self.postal_code})"


class Address(models.Model):
    id_address = models.AutoField(primary_key=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=10, null=True, blank=True)
    floor = models.CharField(max_length=10, null=True, blank=True)
    apartment = models.CharField(max_length=10, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE,
        db_column='id_city',
        related_name='addresses'
    )
    date_create = models.DateTimeField(null=True, blank=True)
    date_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'n_address'
        managed = False

    def __str__(self):
        return f"{self.street} {self.number or ''} - {self.city.name if self.city else 'Sin ciudad'}"



class ProviderCity(models.Model):
    provider = models.ForeignKey(
        'Provider',
        on_delete=models.CASCADE,
        db_column='id_provider',
        related_name='provider_cities'
    )
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE,
        db_column='id_city',
        related_name='city_providers'
    )

    class Meta:
        db_table = 'n_provider_city'
        managed = False
        unique_together = ('provider', 'city')  # ya está en el PRIMARY KEY

    def __str__(self):
        return f"{self.provider} - {self.city}"
from django.db import models
from authentication.models import Provider, Customer, User

# ====================================================
# Modelo que representa los posibles "grados" o calificaciones
# ====================================================
class Grade(models.Model):
    id_grade = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    value = models.PositiveSmallIntegerField()  # equivalente a TINYINT

    class Meta:
        db_table = 'n_grade'
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'

    def __str__(self):
        return f"{self.name} ({self.value})"

# ====================================================
# Calificaciones que los Providers dan a los Customers
# ====================================================
class GradeCustomer(models.Model):
    id_grade_customer = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='id_customer',
        related_name='grade_customer_receiver'
    )
    provider = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='id_provider',
        related_name='grade_provider_sender'
    )
    
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    response = models.CharField(max_length=255, null=True, blank=True)
    is_visible = models.BooleanField(default=True)
    user_create = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='gradecustomer_created', db_column='id_user_create'
    )
    user_update = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='gradecustomer_updated', db_column='id_user_update'
    )
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'n_grade_customer'
        verbose_name = 'Grade Customer'
        verbose_name_plural = 'Grade Customers'
        unique_together = ('provider', 'customer')  # evita duplicados
        managed = False  # ponelo en True si querés usar makemigrations/migrate

    def __str__(self):
        return f"Grade {self.rating} for {self.provider} by {self.customer}"

# ====================================================
# Calificaciones que los Customers dan a los Providers
# ====================================================
class GradeProvider(models.Model):
    id_grade_provider = models.AutoField(primary_key=True)
    provider = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_provider', related_name='grade_provider')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_customer', related_name='grade_customer')  # cliente que califica
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, db_column='id_grade')
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    coment = models.CharField(max_length=255, blank=True, null=True)
    response = models.CharField(max_length=255, blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    user_create = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gradeprovider_created', db_column='id_user_create')
    user_update = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gradeprovider_updated', db_column='id_user_update')
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'n_grade_provider'
        verbose_name = 'Grade Provider'
        verbose_name_plural = 'Grade Providers'
        unique_together = ('provider', 'customer')  # evita duplicados por cliente/proveedor

    def __str__(self):
        return f"Grade {self.grade.value} for {self.provider} by {self.customer}"


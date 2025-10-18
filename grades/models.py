from django.db import models
from authentication.models import Provider, Customer, User

class Grade(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    value = models.PositiveSmallIntegerField()  # equivalente a TINYINT

    class Meta:
        db_table = 'n_grade'
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'

    def __str__(self):
        return f"{self.name} ({self.value})"


class GradeProvider(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, db_column='id_provider')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_customer')  # cliente que califica
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, db_column='id_grade')
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    coment = models.CharField(max_length=255)
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


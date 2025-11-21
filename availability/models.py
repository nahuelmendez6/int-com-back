from django.db import models

# Create your models here.
class Availability(models.Model):

    """
    el modelo Availaibility se utiliza para representar la disponibilidad horaria
    de un proveedor.
    
    se define un rango horario start_time - end_time

    cada dia de la semana esta represnetado por enteros del 0 al 6 (0=domingo, 1=lunes, ..., 6=sabado)
    """
    
    DAYS_OF_WEEK = [
        (0, 'Domingo'),
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miércoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
    ]


    id_availability = models.AutoField(primary_key=True)
    id_provider = models.ForeignKey(
        'authentication.Provider',
        on_delete=models.CASCADE,
        db_column='id_provider',
        related_name='availabilities'
    )

    day_of_week = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    id_user_create = models.IntegerField(null=True, blank=True)
    id_user_update = models.IntegerField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'n_availabilities'
        managed = False
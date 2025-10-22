from django.utils import timezone
from django.db import models
from django.forms import ValidationError

from portfolio.models import Material
from petitions.models import Petition

class PostulationState(models.Model):

    """
    Modelo para manejar los estados de las potulaciones
    """


    id_state = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'n_postulation_state'
        managed = False

    def __str__(self):
        return self.name


class Postulation(models.Model):

    """
    Modelo central de postulacion
    """

    id_postulation = models.AutoField(primary_key=True)
    id_petition = models.IntegerField()
    id_provider = models.IntegerField()  # FK a n_provider (puedes crear modelo si quieres)
    winner = models.BooleanField(default=False)
    proposal = models.CharField(max_length=255, null=True, blank=True)
    id_state = models.ForeignKey(
        PostulationState,
        on_delete=models.PROTECT,
        db_column='id_state'
    )
    current = models.CharField(max_length=45, null=True, blank=True)
    id_user_create = models.IntegerField(null=True, blank=True)
    id_user_update = models.IntegerField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'n_postulation'
        managed = False
        

    def clean(self):
        # Traer a la peticion asociada
        try:
            petition = Petition.objects.get(pk=self.id_petition)
        except Petition.DoesNotExist:
            raise ValidationError("La peticion asociada no existe.")
        
        today = timezone.now().date()

        # validacion de fechas
        if petition.date_since and today < petition.date_since:
            raise ValidationError("La postulación aún no está habilitada.")
        if petition.date_until and today > petition.date_until:
            raise ValidationError("La postulacion ya cerró.")
        
        # validacion de unicidad entre postulaciones activas
        if Postulation.objects.filter(
            id_petition=self.id_petition,
            id_provider=self.id_provider,
            is_deleted = False
        ).exists():
            raise ValidationError("Ya tienes una postulación activa para esta petición.")


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'Postulation {self.id_postulation}'


class PostulationBudget(models.Model):

    """
    Modelo para gestionar tipo y y cantidad de costos asociados a una postulación
    """

    COST_TYPE_CHOICES = [
        ('por_hora', 'Por Hora'),
        ('por_proyecto', 'Por Proyecto'),
        ('por_item', 'Por Ítem'),
        ('material', 'Material'),
        ('servicio', 'Servicio'),
        ('mixto', 'Mixto'),
    ]

    id_budget = models.AutoField(primary_key=True)
    id_postulation = models.ForeignKey(
        Postulation,
        on_delete=models.CASCADE,
        db_column='id_postulation',
        related_name='budgets'
    )
    cost_type = models.CharField(max_length=20, choices=COST_TYPE_CHOICES, default='por_proyecto')
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    hours = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    item_description = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id_user_create = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'n_postulation_budget'
        managed = False

    def __str__(self):
        return f'Budget {self.id_budget} (Postulation {self.id_postulation_id})'


class PostulationStateHistory(models.Model):

    """
    Modelo para gestionar el historial de cambios de estado de una potulacion
    """

    id_history = models.AutoField(primary_key=True)
    id_postulation = models.ForeignKey(
        Postulation,
        on_delete=models.CASCADE,
        db_column='id_postulation'
    )
    id_state = models.ForeignKey(
        PostulationState,
        on_delete=models.PROTECT,
        db_column='id_state'
    )
    changed_by = models.IntegerField(null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    date_change = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'n_postulation_state_history'
        managed = False

    def __str__(self):
        return f'History {self.id_history} (Postulation {self.id_postulation_id})'



class PostulationMaterial(models.Model):
    id_postulation_material = models.AutoField(primary_key=True)
    id_postulation = models.ForeignKey(
        Postulation,
        on_delete=models.CASCADE,
        db_column='id_postulation',
        related_name='materials'
    )
    id_material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        db_column='id_material'
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    notes = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'n_postulation_material'
        managed = False

    def __str__(self):
        return f'{self.id_material.name} x {self.quantity} (Postulation {self.id_postulation_id})'

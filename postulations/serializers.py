from rest_framework import serializers
from .models import (
    PostulationState,
    Postulation,
    PostulationBudget,
    PostulationStateHistory,
    PostulationMaterial,
)
from portfolio.models import Material  # según tu import


# ---------- ESTADOS DE POSTULACIÓN ----------
class PostulationStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostulationState
        fields = ['id_state', 'name', 'description']


# ---------- MATERIALES ----------
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id_material', 'name', 'unit_price', 'unit', 'description']


# ---------- PRESUPUESTOS ----------
class PostulationBudgetSerializer(serializers.ModelSerializer):
    cost_type_display = serializers.CharField(source='get_cost_type_display', read_only=True)

    class Meta:
        model = PostulationBudget
        fields = [
            'id_budget',
            'id_postulation',
            'cost_type',
            'cost_type_display',
            'amount',
            'unit_price',
            'quantity',
            'hours',
            'item_description',
            'notes',
            'date_created',
            'id_user_create',
        ]


# ---------- HISTORIAL DE ESTADOS ----------
class PostulationStateHistorySerializer(serializers.ModelSerializer):
    state = PostulationStateSerializer(source='id_state', read_only=True)

    class Meta:
        model = PostulationStateHistory
        fields = [
            'id_history',
            'id_postulation',
            'id_state',
            'state',
            'changed_by',
            'notes',
            'date_change',
        ]


# ---------- MATERIALES ASOCIADOS ----------
class PostulationMaterialSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(source='id_material', read_only=True)

    class Meta:
        model = PostulationMaterial
        fields = [
            'id_postulation_material',
            'id_postulation',
            'id_material',
            'material',
            'quantity',
            'unit_price',
            'total',
            'notes',
        ]


# ---------- POSTULACIÓN PRINCIPAL ----------
class PostulationSerializer(serializers.ModelSerializer):
    state = PostulationStateSerializer(source='id_state', read_only=True)
    budgets = PostulationBudgetSerializer(source='postulationbudget_set', many=True, read_only=True)
    materials = PostulationMaterialSerializer(source='postulationmaterial_set', many=True, read_only=True)
    history = PostulationStateHistorySerializer(source='postulationstatehistory_set', many=True, read_only=True)

    class Meta:
        model = Postulation
        fields = [
            'id_postulation',
            'id_petition',
            'id_provider',
            'winner',
            'proposal',
            'id_state',
            'state',
            'current',
            'id_user_create',
            'id_user_update',
            'date_create',
            'date_update',
            'budgets',
            'materials',
            'history',
        ]

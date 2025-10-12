from rest_framework import serializers
from .models import (
    Postulation,
    PostulationBudget,
    PostulationMaterial,
    PostulationState
)

class PostulationBudgetSerializer(serializers.ModelSerializer):
    id_budget = serializers.IntegerField(required=False)

    class Meta:
        model = PostulationBudget
        fields = [
            'id_budget',
            'cost_type',
            'amount',
            'unit_price',
            'quantity',
            'hours',
            'item_description',
            'notes',
            'date_created',
            'id_user_create'
        ]

class PostulationMaterialSerializer(serializers.ModelSerializer):
    id_postulation_material = serializers.IntegerField(required=False)

    class Meta:
        model = PostulationMaterial
        fields = [
            'id_postulation_material',
            'id_material',
            'quantity',
            'unit_price',
            'total',
            'notes'
        ]

class PostulationSerializer(serializers.ModelSerializer):
    budgets = PostulationBudgetSerializer(many=True, required=False)
    materials = PostulationMaterialSerializer(many=True, required=False)

    class Meta:
        model = Postulation
        fields = [
            'id_postulation',
            'id_petition',
            'id_provider',
            'winner',
            'proposal',
            'id_state',
            'current',
            'id_user_create',
            'id_user_update',
            'date_create',
            'date_update',
            'budgets',
            'materials'
        ]

    def validate(self, data):
        # validar que un porveedor solo pueda postular una vez por petición
        id_petition = data.get('id_petition')
        id_provider = data.get('id_provider')

        if Postulation.objects.filter(id_petition=id_petition, id_provider=id_provider).exists():
            raise serializers.ValidationError(
                "El proveedor ya ha postulado a esta petición."
            )

        return data

    def create(self, validated_data):
        budgets_data = validated_data.pop('budgets', [])
        materials_data = validated_data.pop('materials', [])

        postulation = Postulation.objects.create(**validated_data)

        # Crear presupuestos
        for budget in budgets_data:
            PostulationBudget.objects.create(id_postulation=postulation, **budget)

        # Crear materiales
        for material in materials_data:
            PostulationMaterial.objects.create(id_postulation=postulation, **material)

        return postulation

    def update(self, instance, validated_data):
        budgets_data = validated_data.pop('budgets', [])
        materials_data = validated_data.pop('materials', [])

        # Actualizamos campos de la postulación
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualizar/crear presupuestos
        for budget in budgets_data:
            budget_id = budget.get('id_budget', None)
            if budget_id:
                budget_obj = PostulationBudget.objects.get(pk=budget_id, id_postulation=instance)
                for attr, value in budget.items():
                    if attr != 'id_budget':
                        setattr(budget_obj, attr, value)
                budget_obj.save()
            else:
                PostulationBudget.objects.create(id_postulation=instance, **budget)

        # Actualizar/crear materiales
        for material in materials_data:
            material_id = material.get('id_postulation_material', None)
            if material_id:
                material_obj = PostulationMaterial.objects.get(pk=material_id, id_postulation=instance)
                for attr, value in material.items():
                    if attr != 'id_postulation_material':
                        setattr(material_obj, attr, value)
                material_obj.save()
            else:
                PostulationMaterial.objects.create(id_postulation=instance, **material)

        return instance


class PostulationReadSerializer(serializers.ModelSerializer):
    budgets = PostulationBudgetSerializer(many=True, read_only=True)
    materials = PostulationMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Postulation
        fields = '__all__'
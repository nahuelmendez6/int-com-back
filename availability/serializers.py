from rest_framework import serializers

from .models import Availability
from authentication.models import Provider

class AvailabilitySerializer(serializers.ModelSerializer):
    id_provider = serializers.PrimaryKeyRelatedField(
        queryset=Provider.objects.all()
    )

    class Meta:
        model = Availability
        fields = '__all__' 
        read_only_fields = ('id_user_create', 'id_user_update')

    def create(self, validated_data):
        validated_data['id_user_create'] = self.context['request'].user.id_user
        return super().create(validated_data)


    def validate(self, data):
         # Si es PATCH, usar los valores actuales si no vienen
        start_time = data.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = data.get('end_time', getattr(self.instance, 'end_time', None))
        provider = data.get('id_provider', getattr(self.instance, 'id_provider', None))
        day_of_week = data.get('day_of_week', getattr(self.instance, 'day_of_week', None))


        # Validar rango horario
        if start_time >= end_time:
            raise serializers.ValidationError("start_time debe ser menor que end_time")

        # Validar solapamiento
        qs = Availability.objects.filter(
            id_provider=provider,
            day_of_week=day_of_week,
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        overlap = qs.filter(
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if overlap:
            raise serializers.ValidationError("El rango horario se solapa con otro existente")

        return data

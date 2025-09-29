from rest_framework import serializers

from .models import Availability

class AvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Availability
        fields = '__all__'

    def validate(self, data):
        """
        Validar que start_time sea menor que end_time
        """
        if self.initial_data['start_time'] >= self.initial_data['end_time']:
            raise serializers.ValidationError("start_time debe ser menor que end_time")
        return data
    
        """
        Validar solapamiento
        """
        qs = Availability.objects.filter(
            id_provider=provider,
            day_of_week=day_of_week,
        )

        # Si estamos editando un registro, excluirlo de la busqueda
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        overlap = qs.filter(
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if overlap:
            raise serializers.ValidationError("El rango horario se solapa con otro existente")
        
        return data
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Country, Province, Department, City, Address, ProviderCity
from .serializers import (CountrySerializer,
                          ProvinceSerializer,
                          DepartmentSerializer,
                          CitySerializer,
                          AddressSerializer,
                          ProviderCitySerializer)
# ====================================
# VIEWSET: COUNTRY
# ====================================
class CountryViewSet(viewsets.ModelViewSet):
    
    """
    ViewSet para el modelo Country.
    Permite todas las operaciones CRUD (GET, POST, PUT, DELETE).
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

# ====================================
# VIEWSET: PROVINCE
# ====================================
class ProvinceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Province.
    Permite todas las operaciones CRUD.
    """
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

# ====================================
# VIEWSET: DEPARTMENT
# ====================================
class DepartmentViewSet(viewsets.ModelViewSet):
    
    
    """
    ViewSet para el modelo Department.
    Incluye operación adicional para filtrar por provincia.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @action(detail=False, methods=['get'], url_path='by-province/(?P<province_id>[^/.]+)')
    def by_province(self, request, province_id=None):

        """
        Retorna todos los departamentos de una provincia específica.
        URL: /departments/by-province/<province_id>/
        """
        departments = Department.objects.filter(province_id=province_id)
        serializer = self.get_serializer(departments, many=True)
        return Response(serializer.data)

# ====================================
# VIEWSET: CITY
# ====================================
class CityViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo City.
    Incluye operación adicional para filtrar por departamento.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer

    @action(detail=False, methods=['get'], url_path='by-department/(?P<department_id>[^/.]+)')
    def by_department(self, request, department_id=None):

        """
        Retorna todas las ciudades de un departamento específico.
        URL: /cities/by-department/<department_id>/
        """
        cities = City.objects.filter(department_id=department_id)
        serializer = self.get_serializer(cities, many=True)
        return Response(serializer.data)

# ====================================
# VIEWSET: ADDRESS
# ====================================
class AddressViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Address.
    Permite todas las operaciones CRUD.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

# ====================================
# API VIEW: PROVIDER CITIES (LISTADO)
# ====================================
class ProviderCitiesAPIView(APIView):
    """
    Retorna la lista de ciudades asignadas a un proveedor específico.
    GET /cities-area/<provider_id>/
    """
    def get(self, request, provider_id):
        provider_cities = ProviderCity.objects.filter(provider_id=provider_id).select_related('city')
        cities = [pc.city for pc in provider_cities]
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ====================================
# API VIEW: DELETE PROVIDER-CITY
# ====================================
class ProviderCityDeleteAPIView(APIView):
    
    """
    Elimina la relación entre un proveedor y una ciudad específica.
    DELETE /providers/<provider_id>/cities/<city_id>/
    """
    def delete(self, request, provider_id, city_id):
        print(f"Eliminar relación provider_id={provider_id}, city_id={city_id}")
        deleted_count, _ = ProviderCity.objects.filter(provider_id=provider_id, city_id=city_id).delete()
        if deleted_count == 0:
            return Response({'detail': 'Relación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Relación eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)


# ====================================
# VIEWSET: PROVIDER CITY
# ====================================
class ProviderCityViewSet(viewsets.ModelViewSet):
    
    """
    ViewSet para el modelo ProviderCity (relación Many-to-Many entre proveedores y ciudades).
    Incluye métodos para crear múltiples relaciones y sincronizar ciudades.
    """
    queryset = ProviderCity.objects.all()
    serializer_class = ProviderCitySerializer

    def create(self, request, *args, **kwargs):
        """
        Permite crear una o varias relaciones proveedor-ciudad.
        Detecta si `request.data` es lista o diccionario.
        """
        is_many = isinstance(request.data, list)  # chequea si es lista o dict
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['patch'], url_path='sync')
    def sync_cities(self, request, *args, **kwargs):
        """
                Sincroniza las ciudades de un provider:
                - Recibe { "provider": id, "cities": [1,2,3] }
                - Borra las que ya no están
                - Crea las nuevas
        """
        provider_id = request.data.get("provider")
        cities = request.data.get("cities", [])

        if not provider_id:
            return Response({"error":"provider es requerido"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Traer las ciudades actuales

        current = ProviderCity.objects.filter(provider_id=provider_id).values_list("city_id", flat=True)

        # Determinar las que hay que borrar y las que hay que crear
        to_delete = set(current) - set(cities)
        to_add = set(cities) - set(current)

        # Borrar las que ya no están
        if to_delete:
            ProviderCity.objects.filter(provider_id=provider_id, city_id__in=to_delete).delete()

        # Crear las nuevas
        new_objs = [ProviderCity(provider_id=provider_id, city_id=cid) for cid in to_add]
        ProviderCity.objects.bulk_create(new_objs, ignore_conflicts=True)

        # Devolver estado actual
        qs = ProviderCity.objects.filter(provider_id=provider_id)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



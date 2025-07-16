from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Country, Province, Department, City, Address, ProviderCity
from .serializers import (CountrySerializer,
                          ProvinceSerializer,
                          DepartmentSerializer,
                          CitySerializer,
                          AddressSerializer,
                          ProviderCitySerializer)

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @action(detail=False, methods=['get'], url_path='by-province/(?P<province_id>[^/.]+)')
    def by_province(self, request, province_id=None):
        departments = Department.objects.filter(province_id=province_id)
        serializer = self.get_serializer(departments, many=True)
        return Response(serializer.data)

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    @action(detail=False, methods=['get'], url_path='by-department/(?P<department_id>[^/.]+)')
    def by_department(self, request, department_id=None):
        cities = City.objects.filter(department_id=department_id)
        serializer = self.get_serializer(cities, many=True)
        return Response(serializer.data)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class ProviderCityViewSet(viewsets.ModelViewSet):
    queryset = ProviderCity.objects.all()
    serializer_class = ProviderCitySerializer

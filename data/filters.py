import django_filters 
from django_filters import CharFilter

from .models import *


class SiswaFilter(django_filters.FilterSet):
    nisn = CharFilter(field_name="nisn", lookup_expr='icontains')
    nama = CharFilter(field_name="nama", lookup_expr='icontains')
    class Meta:
        model = Siswa
        fields = '__all__'


class SPPSiswaFilter(django_filters.FilterSet):
    class Meta:
        model = Sppsiswa
        fields = '__all__'

from django.contrib import admin

# Register your models here.
from django.db import models
from .models import Kelas, Siswa, Spp, Sppsiswa, SppItem, Bendahara

class SiswaAdmin(admin.ModelAdmin):
    list_display = ['nisn', 'user', 'nama', 'namakls']
    search_fields = ['nisn', 'nama']
    list_filter = ('nisn',)
    list_per_page = 10

class SppAdmin(admin.ModelAdmin):
    list_display = ['kelas', 'spp', 'bulan', 'tahun']
    search_fields = ['kelas', 'bulan']
    list_filter = ('kelas',)
    list_per_page = 10

class SppsiswaAdmin(admin.ModelAdmin):
    list_display = ['siswa', 'date', 'lunas', 'url']
    search_fields = ['siswa',]
    list_filter = ('siswa',)
    list_per_page = 10

class SppItemAdmin(admin.ModelAdmin):
    list_display = ['spp', 'sppsiswa', 'siswa', 'quantity', 'date']
    search_fields = ['siswa']
    list_filter = ('siswa',)
    list_per_page = 10

class KelasAdmin(admin.ModelAdmin):
    list_display = ['id', 'namakls']
    search_fields = ['namakls']
    list_filter = ('id',)
    list_per_page = 10

class BendaharaAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'namapetugas']
    search_fields = ['user', 'namapetugas']
    list_filter = ('id',)
    list_per_page = 10

admin.site.register(Siswa, SiswaAdmin)
admin.site.register(Spp, SppAdmin)
admin.site.register(Sppsiswa, SppsiswaAdmin)
admin.site.register(SppItem, SppItemAdmin)
admin.site.register(Kelas, KelasAdmin)
admin.site.register(Bendahara, BendaharaAdmin)
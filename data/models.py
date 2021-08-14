from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Kelas(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    namakls = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.namakls

class Siswa(models.Model):
    nisn = models.CharField(max_length=100, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nama = models.CharField(max_length=200, null=True)
    namakls = models.ForeignKey(Kelas, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%s, %s' % (self.nisn, self.nama)


class Spp(models.Model):
    BULAN = (
            ('Januari', 'Januari'),
           	('Februari', 'Februari'),
            ('Maret', 'Maret'),
            ('April', 'April'),
            ('Mei', 'Mei'),
            ('Juni', 'Juni'),
            ('Juli', 'Juli'),
            ('Agustus', 'Agustus'),
            ('September', 'September'),
            ('Oktober', 'Oktober'),
            ('November', 'November'),
            ('Desember', 'Desember'),
    )
    kelas = models.ForeignKey(Kelas, null=True, blank=True, on_delete=models.SET_NULL)
    spp = models.IntegerField(null=True)
    bulan = models.CharField(max_length=200, null=True, choices=BULAN)
    tahun = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return '%s, %s, %s' % (self.kelas, self.bulan, self.tahun)

class Sppsiswa(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    lunas = models.BooleanField(default=False)
    url = models.CharField(max_length=200, default="0", blank=True, null=True)

    def __str__(self):
        return '%s, %s' % (self.siswa, self.lunas)

    @property
    def get_cart_total(self):
        sppitems = self.sppitem_set.all()
        total = sum([item.get_total for item in sppitems])
        return total

    @property
    def get_cart_item(self):
        sppitems = self.sppitem_set.all()
        total = sum([item.quantity for item in sppitems])
        return total


class SppItem(models.Model):
    spp = models.ForeignKey(Spp, on_delete=models.SET_NULL, null=True, blank=True)
    sppsiswa = models.ForeignKey(Sppsiswa, on_delete=models.CASCADE, null=True)
    siswa = models.ForeignKey(Siswa, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s, %s' % (self.spp, self.sppsiswa)

    @property
    def get_total(self):
        total = self.spp.spp * self.quantity
        return total

class Bendahara(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    namapetugas = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user
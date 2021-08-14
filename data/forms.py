from django import forms
from django.forms import ModelForm
from .models import Siswa, Kelas, Sppsiswa, User, Spp, SppItem, Bendahara
from django.contrib.auth.forms import UserCreationForm


class SisForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIS'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Siswa'}),
            'password1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Konfirmasi Password'}),
        }
        labels = {
            'username': 'NISN',
            'first_name': 'Nama',
            'last_name': 'Kelas',
        }


class SiswaForm(ModelForm):
    class Meta:
        model = Siswa
        fields = '__all__'
        widgets = {
            'nisn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NISN'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Siswa'}),
            'namakls': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nisn': 'Nomor Induk Siswa',
            'nama': 'Nama',
            'namakls': 'Nama Kelas',

        }


class KelasForm(ModelForm):
    class Meta:
        model = Kelas
        fields = '__all__'
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'namakls': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'id': 'ID Kelas',
            'namakls': 'Nama Kelas',

        }


class SppSiswaForm(ModelForm):
    class Meta:
        model = Sppsiswa
        fields = '__all__'
        widgets = {
            'siswa': forms.Select(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'siswa': 'Nama Siswa',
            'lunas': 'Lunas',
            'url': 'Link Bayar',

        }


class SppForm(ModelForm):
    class Meta:
        model = Spp
        fields = '__all__'
        widgets = {
            'kelas': forms.Select(attrs={'class': 'form-control'}),
            'spp': forms.TextInput(attrs={'class': 'form-control'}),
            'bulan': forms.Select(attrs={'class': 'form-control'}),
            'tahun': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'kelas': 'Kelas Siswa',
            'spp': 'Nominal SPP Siswa',
            'bulan': 'Bulan',
            'tahun': 'Tahun',

        }


class SPPitemForm(ModelForm):
    class Meta:
        model = SppItem
        fields = '__all__'
        widgets = {
            'spp': forms.Select(attrs={'class': 'form-control'}),
            'sppsiswa': forms.Select(attrs={'class': 'form-control'}),
            'siswa': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Isi dengan angka 1'}),
        }
        labels = {
            'spp': 'Pilih Bulan',
            'sppsiswa': 'Pilih Status',
            'siswa': 'Nama Siswa',
            'quantity': 'Jumlah',

        }

class PetugasForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'password', 'groups']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIP'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
        labels = {
            'username': 'NIP',
            'first_name': 'Nama',
            'password': 'Password',
            'groups': 'Level',
        }
class UPetugasForm(ModelForm):
    class Meta:
        model = Bendahara
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'namapetugas': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'UserName',
            'namapetugas': 'Nama Petugas'
        }
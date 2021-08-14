from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404

def tolakhalaman_ini(fungsi_awal):
    def perubahan_halaman(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return fungsi_awal(request, *args, **kwargs)
    return perubahan_halaman


def ijinkan_pengguna(yang_diizinkan=['admin']):
    def aturan(fungsi_awal):
        def perubahan_halaman(request, *args, **kwargs):
            # print('Nama User', yang_diizinkan )
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in yang_diizinkan:
                return fungsi_awal(request, *args, **kwargs)
            else:
                return HttpResponse('< h2 > <center > Anda Tidak Dijikankan Ke Tampilan ini < /center > </h2 >')
        return perubahan_halaman
    return aturan


def pilihan_login(fungsi_awal):
    def perubahan_halaman(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'siswa':
            return redirect('siswapage')
        if group == 'admin':
            return fungsi_awal(request, *args, **kwargs)
    return perubahan_halaman
